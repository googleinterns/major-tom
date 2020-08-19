import React from 'react'
import { AppBar, Toolbar, Avatar, Input, IconButton, Fade, LinearProgress } from '@material-ui/core'
import { Search as SearchIcon } from '@material-ui/icons'
import styles from './styles'

const SearchBar = ({ setSearch, refetch, setLoading, loading }) => {
  const classes = styles()

  return (
    <AppBar position='sticky' color='inherit' className={classes.appbar}>
      <Toolbar>
        <div className={classes.search}>
          <IconButton
            aria-label='search'
            color='inherit'
            className={classes.searchIcon}
            onClick={() => refetch()}
          >
            <SearchIcon />
          </IconButton>
          <Input
            type='search'
            placeholder='Buscar...'
            classes={{
              root: classes.inputRoot,
              input: classes.inputInput
            }}
            onChange={({ target: { value } }) => {
              if (value?.length !== 0) {
                setLoading(true)
                setSearch(value)
              } else {
                setLoading(false)
              }
            }}
          />
        </div>
        <Avatar alt='Reglamento Vial' src='/static/icon-bg.png' className={classes.avatar} />
      </Toolbar>
      {(loading &&
        <Fade in={loading} style={{ transitionDelay: '1200ms' }}>
          <LinearProgress />
        </Fade>
      )}
    </AppBar>
  )
}

export default SearchBar
