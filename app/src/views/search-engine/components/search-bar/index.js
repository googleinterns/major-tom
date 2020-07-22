import React from 'react';
import { AppBar, Toolbar, Avatar, Input } from '@material-ui/core';
import styles from './styles';

const SearchBar = ({ setSearch }) => {
  const classes = styles();

  return (
    <AppBar position="sticky" color="inherit" className={classes.appbar}>
      <Toolbar>
        <div className={classes.search}>
          <Input
            type="search"
            placeholder="Buscar..."
            classes={{
              root: classes.inputRoot,
              input: classes.inputInput,
            }}
            onChange={({ target: { value } }) => setSearch(value)}
          />
        </div>
        <Avatar alt="Reglamento Vial" src="/static/icon-bg.png" className={classes.avatar} />
      </Toolbar>
    </AppBar>
  );
};

export default SearchBar;
