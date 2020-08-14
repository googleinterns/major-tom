import 'babel-polyfill'
import path from 'path'
import { ApolloServer, gql } from 'apollo-server'
import { describe, expect, test } from '@jest/globals'
import { importSchema } from 'graphql-import'
import { createTestClient } from 'apollo-server-testing'
import resolvers from './mock-resolvers'
import { GraphQLError } from 'graphql'

const typeDefs = importSchema(path.join(__dirname, './mock-typedefs/index.graphql'))
const server = new ApolloServer({ typeDefs, resolvers })

const tests = [
  {
    name: 'Normal request with a valid search',
    query: gql`
            query articles($search: String! $limit: Int) {
                articles(search: $search limit: $limit) {
                    id
                    number
                    content
                    keywords
                    minutesToRead
                }
            }
        `,
    variables: { search: 'Es obligatorio usar casco con bicicleta?', limit: 3 },
    expected: {
      articles: [{
        id: '1',
        number: 1,
        content:
                    'Esta prohibido manejar en las siguientes condiciones:\n\t 1. Teniendo los faros rotos\n\t 2. Teniendo las llantas ponchadas\nCualquiera de estos casos no será tolerado!',
        keywords: [
          'Lorem',
          'Ipsum',
          'Ipsum',
          'Ipsum',
          'Ipsum',
          'Ipsum',
          'Ipsum',
          'Ipsum',
          'Ipsum',
          'Ipsum'
        ],
        minutesToRead: 5
      }, {
        id: '2',
        number: 2,
        content:
                        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        keywords: ['Lorem', 'Ipsum'],
        minutesToRead: 10
      }, {
        id: '3',
        number: 3,
        content:
                        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        keywords: ['Lorem', 'Ipsum'],
        minutesToRead: 8
      }]
    }
  },
  {
    name: 'Specific attributes to select',
    query: gql`
            query articles($search: String! $limit: Int) {
                articles(search: $search limit: $limit) {
                    number
                    content
                }
            }
        `,
    variables: { search: '', limit: 3 },
    expected: {
      articles: [{
        id: '1',
        number: 1,
        content:
                    'Esta prohibido manejar en las siguientes condiciones:\n\t 1. Teniendo los faros rotos\n\t 2. Teniendo las llantas ponchadas\nCualquiera de estos casos no será tolerado!',
        keywords: [
          'Lorem',
          'Ipsum',
          'Ipsum',
          'Ipsum',
          'Ipsum',
          'Ipsum',
          'Ipsum',
          'Ipsum',
          'Ipsum',
          'Ipsum'
        ],
        minutesToRead: 5
      }, {
        id: '2',
        number: 2,
        content:
                    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        keywords: ['Lorem', 'Ipsum'],
        minutesToRead: 10
      }, {
        id: '3',
        number: 3,
        content:
                    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        keywords: ['Lorem', 'Ipsum'],
        minutesToRead: 8
      }].map(({ number, content }) => ({ number, content }))
    }
  },
  {
    name: 'None match from request',
    query: gql`
            query articles($search: String! $limit: Int) {
                articles(search: $search limit: $limit) {
                    id
                    number
                    content
                    keywords
                    minutesToRead
                }
            }
        `,
    variables: { search: 'A very thorough search that won\'t return anything...', limit: 0 },
    expected: { articles: [] }
  },
  {
    name: 'Search error',
    query: gql`
            query articlesSearchError($search: String!) {
                articlesSearchError(search: $search) {
                    id
                }
            }
        `,
    variables: { search: '' },
    expected: [new GraphQLError(JSON.stringify({ message: 'This is the error message', trace: 'unicode ugly stack trace' }))]
  },
  {
    name: 'Article in database does not exists',
    query: gql`
            query articles($search: String! $limit: Int) {
                articles(search: $search limit: $limit) {
                    id
                }
            }
        `,
    variables: { search: '', limit: 20 },
    expected: [new GraphQLError(JSON.stringify({ error: 'No article matches such ID', code: 404 }))]
  }
]

describe('Article Queries', () => {
  const client = createTestClient(server)

  tests.forEach(currentTest => {
    const { name, query, variables, expected } = currentTest

    test(`query: ${name}`, async () => {
      const results = await client.query({ query, variables })
      if (results.errors) {
        return expect(results.errors).toEqual(expected)
      }
      return expect(results.data).toEqual(expected)
    })
  })
})
