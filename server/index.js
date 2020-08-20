import { ApolloServer } from 'apollo-server'
import { importSchema } from 'graphql-import'
import path from 'path'
import redis from 'async-redis'
import localCache from './utils/in-memory-cache'
import resolvers from './resolvers'
import { PORT, REDIS_IP, REDIS_PORT } from './config'

const typeDefs = importSchema(path.join(__dirname, './typedefs/index.graphql'))

// If you don't want to spin up a local Redis server, make sure to avoid
// REDIS_IP and REDIS_PORT .env variables declared to default to an in-memory storage
const cache = REDIS_IP && REDIS_PORT
  ? redis.createClient({ host: REDIS_IP, port: REDIS_PORT })
  : localCache

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req = {}, res }) => ({ req, res, cache }),
  introspection: true,
  playground: true
})

cache.on('ready', isLocal => {
  console.log(isLocal || `🧶  Redis server ready at ${REDIS_IP}:${REDIS_PORT}`)
  server.listen(PORT).then(({ url }) => console.log(`🚀  Server ready at ${url}`))
})
