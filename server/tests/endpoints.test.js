import 'babel-polyfill'
import axios from 'axios'
import { describe, expect, jest, test } from '@jest/globals'
import { databaseApi, searchApi } from '../endpoints'
import { articles } from './mocks'
import { DATABASE_ENDPOINT, SEARCH_ENDPOINT } from '../config'

jest.mock('axios')

const searchApiTests = [
  {
    name: 'Successful search with multiple results',
    query: 'A random query',
    response: Promise.resolve([1, 2, 3]),
    expected: [1, 2, 3]
  },
  {
    name: 'Successful query with single result',
    query: 'A random query',
    response: Promise.resolve([1]),
    expected: [1]
  },
  {
    name: 'Search error',
    query: 'A random query',
    response: Promise.resolve({ error: { message: 'An error message', trace: 'Its stack trace' } }),
    expected: { error: { message: 'An error message', trace: 'Its stack trace' } }
  }
]

const databaseApiTests = [
  {
    name: 'Successful article response from id',
    id: 1,
    expected: articles[0]
  },
  {
    name: 'Article id does not exists',
    id: 20,
    expected: { error: 'No article matches such ID', code: 404 }
  }
]

describe('Endpoint tests', () => {
  searchApiTests.forEach(currentTest => {
    const { name, query, response, expected } = currentTest

    test(`query: ${name}`, async () => {
      axios.post.mockImplementation((url, data) => {
        expect(url).toEqual(SEARCH_ENDPOINT)
        expect(data).toEqual({ query })
        return response
      })
      const results = await searchApi(query)
      return expect(results).toEqual(expected)
    })
  })

  databaseApiTests.forEach(currentTest => {
    axios.get.mockImplementation(url => {
      expect(url).toMatch(new RegExp(`^${DATABASE_ENDPOINT}/[0-9a-zA-Z\\-_]+$`))

      const urlTokens = url.toString().split('/')
      const id = urlTokens[urlTokens.length - 1]
      for (const article of articles) {
        if (article.id === id) {
          return article
        }
      }

      return { error: 'No article matches such ID', code: 404 }
    })

    const { name, id, expected } = currentTest

    test(`query: ${name}`, async () => {
      const results = await databaseApi(id)
      return expect(results).toEqual(expected)
    })
  })
})
