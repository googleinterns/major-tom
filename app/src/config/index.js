import dotenv from 'dotenv'

dotenv.config()

const HTTP_URI = process.env.REACT_APP_HTTP_URI

export { HTTP_URI }
