import { ApolloClient, InMemoryCache } from '@apollo/client'
import { HTTP_URI } from '../config'

const client = new ApolloClient({
  uri: HTTP_URI,
  cache: new InMemoryCache(),
  defaultOptions: {
    query: {
      fetchPolicy: 'network-only',
      errorPolicy: 'all'
    },
    mutate: {
      errorPolicy: 'all'
    }
  }
})

export default client
