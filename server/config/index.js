import dotenv from 'dotenv'

dotenv.config()

const { PORT } = process.env
const { SEARCH_ENDPOINT } = process.env
const { DATABASE_ENDPOINT } = process.env

export { PORT, SEARCH_ENDPOINT, DATABASE_ENDPOINT }
