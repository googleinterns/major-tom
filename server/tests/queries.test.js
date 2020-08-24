import 'babel-polyfill'
import path from 'path'
import { GraphQLError } from 'graphql'
import { ApolloServer, gql } from 'apollo-server-express'
import { describe, expect, jest, test } from '@jest/globals'
import { importSchema } from 'graphql-import'
import { createTestClient } from 'apollo-server-testing'
import resolvers from '../resolvers'
import { databaseApi, searchApi } from '../endpoints'
import { mockArticles, mockArticlesInCache } from './mocks'

// In-memory cache to mock redis operations
const cache = new Map()
cache.exists = key => cache.has(key)

const typeDefs = importSchema(path.join(__dirname, '../typedefs/index.graphql'))
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req = {}, res }) => ({ req, res, cache })
})

const tests = [
  {
    name: 'Normal request with a valid search',
    query: gql`
            query articles($search: String!) {
                articles(search: $search) {
                    id
                    number
                    content
                    keywords
                    minutesToRead
                }
            }
        `,
    variables: { search: 'Es obligatorio usar casco con bicicleta?' },
    initialCache: [],
    response: { data: { articles: ['1'] } },
    expected: { articles: [mockArticles[0]] },
    expectedCalls: [['1']]
  },
  {
    name: 'Normal request with a valid search and multiple results',
    query: gql`
            query articles($search: String!) {
                articles(search: $search) {
                    id
                    number
                    content
                    keywords
                    minutesToRead
                }
            }
        `,
    variables: { search: 'Es obligatorio usar casco con bicicleta?' },
    initialCache: [],
    response: { data: { articles: ['2', '3', '4'] } },
    expected: { articles: [mockArticles[1], mockArticles[2], mockArticles[3]] },
    expectedCalls: [['2'], ['3'], ['4']]
  },
  {
    name: 'Normal request with a valid search and multiple results and warm cache',
    query: gql`
        query articles($search: String!) {
            articles(search: $search) {
                id
                number
                content
                keywords
                minutesToRead
            }
        }
    `,
    variables: { search: 'Es obligatorio usar casco con bicicleta?' },
    initialCache: [mockArticlesInCache[4], mockArticlesInCache[5]],
    response: { data: { articles: ['5', '6', '7'] } },
    expected: { articles: [mockArticlesInCache[4], mockArticlesInCache[5], mockArticlesInCache[6]] },
    expectedCalls: [['7']]
  },
  {
    name: 'None match from request',
    query: gql`
            query articles($search: String!) {
                articles(search: $search) {
                    id
                    number
                    content
                    keywords
                    minutesToRead
                }
            }
        `,
    variables: { search: 'A very thorough search that won\'t return anything...' },
    initialCache: [],
    response: { data: { articles: [] } },
    expected: { articles: [] },
    expectedCalls: []
  },
  {
    name: 'Search error',
    query: gql`
            query articles($search: String!) {
                articles(search: $search) {
                    id
                }
            }
        `,
    variables: { search: '' },
    initialCache: [],
    response: { error: { message: 'An error message', trace: 'Its stack trace' } },
    expected: [new GraphQLError(JSON.stringify({ message: 'An error message', trace: 'Its stack trace' }))],
    expectedCalls: []
  },
  {
    name: 'Article in database does not exists',
    query: gql`
            query articles($search: String!) {
                articles(search: $search) {
                    id
                }
            }
        `,
    variables: { search: '' },
    initialCache: [],
    response: { data: { articles: ['20'] } },
    expected: [new GraphQLError(JSON.stringify({ message: 'No article matches such ID', code: 404 }))],
    expectedCalls: []
  }
]

jest.mock('../endpoints')

describe('Queries', () => {
  const client = createTestClient(server)

  test.each(tests)('Test', async ({ query, variables, initialCache, response, expected, expectedCalls }) => {
    jest.clearAllMocks()

    initialCache.forEach(article => cache.set(article.id, JSON.stringify(article)))

    searchApi.mockImplementation(() => response)
    databaseApi.mockImplementation(id => {
      expect(cache.exists(id)).toBeFalsy() // Verify that the article is not already in the cache.

      for (const article of mockArticles) {
        if (article.id === id) {
          return { data: article }
        }
      }

      return { error: { message: 'No article matches such ID', code: 404 } }
    })

    const results = await client.query({ query, variables })
    if (results.errors) {
      return expect(results.errors).toEqual(expected)
    }

    expect(databaseApi.mock.calls).toEqual(expectedCalls)

    // Format resulting article as how they should be stored in the cache
    const cacheToExpect = new Map(results.data.articles.map(article => ([article.id, JSON.stringify({ ...article })])))

    expect(cache).toEqual(cacheToExpect)
    cache.clear()

    return expect(results.data).toEqual(expected)
  })
})
