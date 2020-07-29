import React, { useState, useEffect } from 'react'
import { useQuery } from '@apollo/client'
import { useDebounce } from 'use-lodash-debounce'
import { Container } from '@material-ui/core'
import SearchBar from './components/search-bar'
import ArticlesList from './components/articles-list'
import { GET_ARTICLES } from './graphql/queries'

const SearchEngine = () => {
  const [articles, setArticles] = useState([])
  const [search, setSearch] = useState('')
  const debouncedSearch = useDebounce(search, 1000)
  const getArticlesQuery = useQuery(GET_ARTICLES, { variables: { search: debouncedSearch } })

  useEffect(() => {
    const { data } = getArticlesQuery

    if (data?.articles) {
      setArticles(data.articles)
    }
  }, [debouncedSearch, getArticlesQuery])

  return (
    <Container>
      <SearchBar setSearch={setSearch} refetch={getArticlesQuery.refetch} />
      <ArticlesList articles={articles} />
    </Container>
  )
}

export default SearchEngine
