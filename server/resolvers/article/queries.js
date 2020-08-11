import axios from 'axios'
import { SEARCH_SERVICE_ENDPOINT } from '../../config'

const articleQueries = {
  articles: async (_, { search }) => {
    const database = [
      {
        id: 1,
        number: 1,
        content:
            'El conductor y ocupante de bicicleta, bicimoto o triciclos poder utilizar de preferencia casco de proteccion para el seguridad.',
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
      },
      {
        id: 2,
        number: 2,
        content:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        keywords: ['Lorem', 'Ipsum'],
        minutesToRead: 10
      },
      {
        id: 3,
        number: 3,
        content:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        keywords: ['Lorem', 'Ipsum'],
        minutesToRead: 8
      },
      {
        id: 4,
        number: 4,
        content:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        keywords: ['Lorem', 'Ipsum'],
        minutesToRead: 8
      },
      {
        id: 5,
        number: 5,
        content:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        keywords: ['Lorem', 'Ipsum'],
        minutesToRead: 8
      },
      {
        id: 6,
        number: 6,
        content:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        keywords: ['Lorem', 'Ipsum'],
        minutesToRead: 8
      },
      {
        id: 7,
        number: 7,
        content:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        keywords: ['Lorem', 'Ipsum'],
        minutesToRead: 8
      },
      {
        id: 8,
        number: 8,
        content:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        keywords: ['Lorem', 'Ipsum'],
        minutesToRead: 8
      },
      {
        id: 9,
        number: 9,
        content:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        keywords: ['Lorem', 'Ipsum'],
        minutesToRead: 8
      }
    ]
    const { data } = await axios.post(SEARCH_SERVICE_ENDPOINT, { query: search })
    const articleIds = [...data.articles]

    const articles = []
    for (const id of articleIds) {
      for (const article of database) {
        if (id === article.id) { articles.push(article) }
      }
    }

    return articles
  }
}

export default articleQueries
