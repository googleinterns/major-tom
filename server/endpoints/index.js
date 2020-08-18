import axios from 'axios'
import { DATABASE_ENDPOINT, SEARCH_ENDPOINT } from '../config'

const searchApi = query => axios.post(SEARCH_ENDPOINT, { query })
const databaseApi = id => axios.get(`${DATABASE_ENDPOINT}/${id}`)

export { searchApi, databaseApi }
