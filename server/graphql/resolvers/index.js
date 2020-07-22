// Test
import articleQueries from './article/queries';

const resolvers = {
  Query: {
    ...articleQueries,
  },
};

export default resolvers;
