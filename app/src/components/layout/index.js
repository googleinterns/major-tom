import React from 'react';
import PropTypes from 'prop-types';
import { Container } from '@material-ui/core';

const Layout = ({ children }) => {
  return <Container maxWidth="lg">{children}</Container>;
};

Layout.propTypes = {
  children: PropTypes.any.isRequired,
};

export default Layout;
