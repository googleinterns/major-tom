import { AVERAGE_WORDS_PER_MINUTE } from '../../utils/constants'
import { databaseApi, searchApi } from '../../endpoints'

const articleQueries = {
  articles: async (_, { search }) => {
    const payload = await searchApi(search)

    if (payload.error) return new Error(JSON.stringify(payload.error))

    const articleIds = [...payload.data.articles]
    const articles = []

    const requests = articleIds.map(id => databaseApi(id))
    const articlePayloads = await Promise.all(requests)

    for (const article of articlePayloads) {
<<<<<<< HEAD
      if (article.error) return new Error(JSON.stringify(article))
=======
      if (article.error) return new Error(JSON.stringify(article.error))
>>>>>>> 2dfe2cb94b7ac4d63550d86750dff737c8d8e278

      article.minutesToRead = parseInt(article.wordCount) / AVERAGE_WORDS_PER_MINUTE
      delete article.wordCount

      articles.push(article)
    }

    return articles
  }
}

export default articleQueries
