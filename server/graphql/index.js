import { ApolloServer } from 'apollo-server';
import { importSchema } from 'graphql-import';
import path from 'path';
import resolvers from './resolvers';

const typeDefs = importSchema(path.join(__dirname, './typedefs/index.graphql'));

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req = {}, res }) => ({ req, res }),
});

export default server;
