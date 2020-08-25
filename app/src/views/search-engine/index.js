import React, { useState, useEffect } from 'react'
import { useQuery } from '@apollo/client'
import { useDebounce } from 'use-lodash-debounce'
import { Card, CardContent, Container, Snackbar, Chip, Typography } from '@material-ui/core'
import { Alert } from '@material-ui/lab'
import SearchBar from './components/search-bar'
import ArticlesList from './components/articles-list'
import { GET_ARTICLES } from './graphql/queries'
import styles from './styles'

const SearchEngine = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(undefined)
  const [articles, setArticles] = useState([])
  const [search, setSearch] = useState('')
  const debouncedSearch = useDebounce(search, 1000)
  const getArticlesQuery = useQuery(GET_ARTICLES, { variables: { search: debouncedSearch } })
  const classes = styles()
  const DOC_URL = 'https://www.guadalupe.gob.mx/nuevo-reglamento-de-transito-homologado/'

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
      <Chip
        size='small'
        label={`${articles.length} resultados`}
        className={classes.resultsChip}
      />
      <ArticlesList articles={articles} />
      {articles.length === 0 &&
        <Card className={classes.card}>
          <CardContent>
            <Typography gutterBottom variant='h5' component='h2'>
                Motor de búsqueda - Reglamento Vial de Monterrey
            </Typography>
            <Typography
              variant='body1'
              color='textSecondary'
              component='p'
              className={classes.cardContent}
            >
                Algoritmo para realizar búsquedas optimizadas sobre los <b>reglamentos viales oficiales</b> de tu comunidad.
                El motor de búsqueda intentará encontrar los artículos <u>más relevantes para tu búsqueda</u>.
            </Typography>
            <Typography
              variant='body1'
              color='textSecondary'
              component='p'
              className={classes.cardContent}
            >
                Intenta buscar: <mark>Licencia de conducir</mark>
            </Typography>
            <Typography
              variant='body2'
              color='textSecondary'
              component='p'
              className={classes.cardContent}
            >
                Ahorita estás buscando en:
            </Typography>
            <a href={DOC_URL} target='_blank' rel='noopener noreferrer'>
                REGLAMENTO DE TRÁNSITO Y VIALIDAD DEL MUNICIPIO DE GUADALUPE, NUEVO LEÓN
            </a>
          </CardContent>
        </Card>}
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
