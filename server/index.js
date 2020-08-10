import { ApolloServer } from 'apollo-server'
import { importSchema } from 'graphql-import'
import path from 'path'
import resolvers from './resolvers'
import { PORT } from './config'

const typeDefs = importSchema(path.join(__dirname, './typedefs/index.graphql'))

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req = {}, res }) => ({ req, res }),
  introspection: true,
  playground: true
})

server.listen(PORT).then(({ url }) => {
  console.log(`🚀  Server ready at ${url}`)
})
