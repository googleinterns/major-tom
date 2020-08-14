import { responses } from '../../mocks'
import { AVERAGE_WORDS_PER_MINUTE } from '../../../utils/constants'

const articleQueries = {
  articles: async (_, { limit }) => {
    const payload = responses.articleIdsFromSearch(limit)

    if (!payload.error) {
      const articleIds = [...payload.data.articles]
      const articles = []
      for (const id of articleIds) {
        const article = responses.articleFromIdDatabase(id)

        if (article.error) return new Error(JSON.stringify(article))

        article.minutesToRead = parseInt(article.wordCount) / AVERAGE_WORDS_PER_MINUTE
        delete article.wordCount

        articles.push(article)
      }

      return articles
    }

    return new Error(JSON.stringify(payload.error))
  },
  articlesSearchError: async () => {
    const payload = responses.errorResponseFromSearch()

    if (!payload.error) {
      const articleIds = [...payload.data.articles]
      const articles = []

      for (const id of articleIds) {
        const article = responses.articleFromIdDatabase(id)

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
