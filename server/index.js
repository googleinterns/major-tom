import { ApolloServer } from 'apollo-server-express'
import { importSchema } from 'graphql-import'
import express from 'express'
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

const app = express()
server.applyMiddleware({ app })

app.listen({ port: PORT }, () => {
  console.log(`🚀  Server ready at http://localhost:${PORT}${server.graphqlPath}`)
})
