import { ApolloServer } from 'apollo-server'
import { importSchema } from 'graphql-import'
import path from 'path'
import redis from 'async-redis'
import resolvers from './resolvers'
import { PORT, REDIS_IP, REDIS_PORT } from './config'

const typeDefs = importSchema(path.join(__dirname, './typedefs/index.graphql'))

const cache = redis.createClient({ host: REDIS_IP, port: REDIS_PORT })

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req = {}, res }) => ({ req, res, cache }),
  introspection: true,
  playground: true
})

cache.on('ready', () => console.log(`🧶  Redis server ready at ${REDIS_IP}:${REDIS_PORT}`))

server.listen(PORT).then(({ url }) => console.log(`🚀  Server ready at ${url}`))
