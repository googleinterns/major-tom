import React from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';
import Loadable from 'react-loadable';
import TopBarProgress from 'react-topbar-progress-indicator';
import Layout from 'components/layout';

/* webpackChunkName: "SearchEngine" */
const SearchEngine = Loadable({
  loader: () => import('./views/search-engine'),
  loading: TopBarProgress,
});

const App = () => {
  return (
    <Switch>
      <Layout>
        <Route exact path="/" component={SearchEngine} />
        <Redirect to="/" />
      </Layout>
    </Switch>
  );
};

export default App;
