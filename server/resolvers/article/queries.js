import { AVERAGE_WORDS_PER_MINUTE } from '../../utils/constants'
import { databaseApi, searchApi } from '../../endpoints'

const articleQueries = {
  articles: async (_, { search }) => {
    const payload = await searchApi(search)

    if (payload.error) return new Error(JSON.stringify(payload.error))

    const articleIds = [...payload.data.articles]
    const articles = []

    for (const id of articleIds) {
      const article = await databaseApi(id)

      if (article.error) return new Error(JSON.stringify(article))

      article.minutesToRead = parseInt(article.wordCount) / AVERAGE_WORDS_PER_MINUTE
      delete article.wordCount

      articles.push(article)
    }

    return articles
  }
}

export default articleQueries
