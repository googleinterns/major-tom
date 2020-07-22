import server from './graphql';
import { PORT } from './config';

server.listen(PORT).then(({ url }) => {
  console.log(`🚀  Server ready at ${url}`);
});
