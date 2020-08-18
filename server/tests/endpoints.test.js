import 'babel-polyfill'
import axios from 'axios'
import { describe, expect, jest, test } from '@jest/globals'
import { databaseApi, searchApi } from '../endpoints'
import { DATABASE_ENDPOINT, SEARCH_ENDPOINT } from '../config'
import { mockArticles } from './mocks'

jest.mock('axios')

const searchApiTests = [
  {
    name: 'Search URL',
    expected: SEARCH_ENDPOINT
  }
]

const databaseApiTests = [
  {
    name: 'Database URL',
    expected: DATABASE_ENDPOINT
  }
]

describe('Endpoint tests', () => {
  searchApiTests.forEach(currentTest => {
    const { name, expected } = currentTest

    test(`query: ${name}`, async () => {
      axios.post.mockImplementation(url => {
        expect(url).toEqual(expected)
        return [1, 2, 3]
      })
      return await searchApi('A random request')
    })
  })

  databaseApiTests.forEach(currentTest => {
    const { name, expected } = currentTest

    test(`query: ${name}`, async () => {
      axios.get.mockImplementation(url => {
        expect(url).toMatch(new RegExp(`^${expected}/[0-9a-zA-Z\\-_]+$`))
        return mockArticles[0]
      })
      return await databaseApi(1)
    })
  })
})
