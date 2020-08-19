import 'babel-polyfill'
import path from 'path'
import { GraphQLError } from 'graphql'
import { ApolloServer, gql } from 'apollo-server'
import { describe, expect, jest, test } from '@jest/globals'
import { importSchema } from 'graphql-import'
import { createTestClient } from 'apollo-server-testing'
import resolvers from '../resolvers'
import { databaseApi, searchApi } from '../endpoints'
import { mockArticles } from './mocks'

const typeDefs = importSchema(path.join(__dirname, '../typedefs/index.graphql'))
const server = new ApolloServer({ typeDefs, resolvers })

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
    response: { data: { articles: ['1'] } },
    expected: { articles: [mockArticles[0]] }
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
    response: { data: { articles: ['2', '3', '4'] } },
    expected: { articles: [mockArticles[1], mockArticles[2], mockArticles[3]] }
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
    response: { data: { articles: [] } },
    expected: { articles: [] }
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
    response: { error: { message: 'An error message', trace: 'Its stack trace' } },
    expected: [new GraphQLError(JSON.stringify({ message: 'An error message', trace: 'Its stack trace' }))]
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
    response: { data: { articles: ['20'] } },
    expected: [new GraphQLError(JSON.stringify({ message: 'No article matches such ID', code: 404 }))]
  }
]

jest.mock('../endpoints')

describe('Queries', () => {
  const client = createTestClient(server)
  databaseApi.mockImplementation(id => {
    for (const article of mockArticles) {
      if (article.id === id) {
        return article
      }
    }
    
    return { error: { message: 'No article matches such ID', code: 404 } }
  })

  tests.forEach(currentTest => {
    const { name, query, variables, response, expected } = currentTest

    test(`query: ${name}`, async () => {
      searchApi.mockImplementation(() => response)

      const results = await client.query({ query, variables })
      if (results.errors) {
        return expect(results.errors).toEqual(expected)
      }
      return expect(results.data).toEqual(expected)
    })
  })
})
