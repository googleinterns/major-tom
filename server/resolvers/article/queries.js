import { AVERAGE_WORDS_PER_MINUTE } from '../../utils/constants'
import { databaseApi, searchApi } from '../../endpoints'

const articleQueries = {
  articles: async (_, { search }, { cache }) => {
    const payload = await searchApi(search)

    if (payload.error) return new Error(JSON.stringify(payload.error))

    const articleIds = [...payload.data.articles]
    const articles = []
    const requests = []

    for (const id of articleIds) {
      if (await cache.exists(id)) {
        const article = await cache.get(id)
        articles.push(JSON.parse(article))
      } else {
        requests.push(databaseApi(id))
      }
    }

    const articlePayloads = await Promise.all(requests)

    for (const payload of articlePayloads) {
      const { data: article } = payload

      if (!article) return new Error('Response format not supported!')

      if (article.error) return new Error(JSON.stringify(article.error))

      article.minutesToRead = parseInt(article.wordCount) / AVERAGE_WORDS_PER_MINUTE
      delete article.wordCount

      cache.set(article.id, JSON.stringify(article))

      articles.push(article)
    }

    return articles
  }
}

export default articleQueries
