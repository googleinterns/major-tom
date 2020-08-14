import axios from 'axios'
import { DATABASE_ENDPOINT, SEARCH_ENDPOINT } from '../../config'
import { AVERAGE_WORDS_PER_MINUTE } from '../../utils/constants'

const articleQueries = {
  articles: async (_, { search }) => {
    const payload = await axios.post(SEARCH_ENDPOINT, { query: search })

    if (!payload.error) {
      const articleIds = [...payload.data.articles]
      const articles = []

      for (const id of articleIds) {
        const article = await axios.get(`${DATABASE_ENDPOINT}/${id}`)

        if (article.error) return new Error(JSON.stringify(article))

        article.minutesToRead = parseInt(article.wordCount) / AVERAGE_WORDS_PER_MINUTE
        delete article.wordCount

        articles.push(article)
      }

      return articles
    }

    return new Error(JSON.stringify(payload.error))
  }
}

export default articleQueries
