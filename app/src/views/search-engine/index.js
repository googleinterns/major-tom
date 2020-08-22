import React, { useState, useEffect } from 'react'
import { useQuery } from '@apollo/client'
import { useDebounce } from 'use-lodash-debounce'
import { Container, Snackbar } from '@material-ui/core'
import { Alert } from '@material-ui/lab'
import SearchBar from './components/search-bar'
import ArticlesList from './components/articles-list'
import { GET_ARTICLES } from './graphql/queries'

const SearchEngine = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(undefined)
  const [articles, setArticles] = useState([])
  const [search, setSearch] = useState('')
  const debouncedSearch = useDebounce(search, 1000)
  const getArticlesQuery = useQuery(GET_ARTICLES, { variables: { search: debouncedSearch } })

  useEffect(() => {
    const { data, error } = getArticlesQuery

    if (error) {
      let errorToSet

      try {
        errorToSet = typeof error === 'object'
          ? error
          : JSON.parse(error.message)
      } catch (e) {
        console.log(error)
      }

      setError(errorToSet)
    } else if (data?.articles) {
      setArticles(data.articles)
    }
    setLoading(false)
  }, [debouncedSearch, getArticlesQuery])

  return (
    <Container>
      <SearchBar
        setSearch={setSearch}
        refetch={getArticlesQuery.refetch}
        setLoading={setLoading}
        loading={loading}
      />
      <ArticlesList articles={articles} />
      <Snackbar
        open={error !== undefined}
        autoHideDuration={2000}
        onClose={() => setError(undefined)}
      >
        <Alert elevation={6} variant='filled' severity='error'>
          {error?.message}
        </Alert>
      </Snackbar>
    </Container>
  )
}

export default SearchEngine
