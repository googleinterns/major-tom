import dotenv from 'dotenv'

dotenv.config()

const { PORT } = process.env
const { SEARCH_ENDPOINT } = process.env
const { DATABASE_ENDPOINT } = process.env
const { REDIS_IP } = process.env
const { REDIS_PORT } = process.env

export { PORT, SEARCH_ENDPOINT, DATABASE_ENDPOINT, REDIS_IP, REDIS_PORT }
