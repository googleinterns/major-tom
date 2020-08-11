import dotenv from 'dotenv'

dotenv.config()

const { PORT } = process.env
const { SEARCH_SERVICE_ENDPOINT } = process.env

export { PORT, SEARCH_SERVICE_ENDPOINT }
