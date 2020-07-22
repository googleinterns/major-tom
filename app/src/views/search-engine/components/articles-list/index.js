import React, { useState } from 'react';
import {
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Card,
  CardContent,
  CardActions,
  Typography,
  Chip,
  Button,
} from '@material-ui/core';
import styles from './styles';

const ArticlesList = ({ articles }) => {
  const [currentArticle, setCurrentArticle] = useState(undefined);
  const classes = styles();

  return (
    <Grid container spacing={3}>
      {articles.map((article) => {
        const contentPreview =
          article.content.length > 200
            ? `${article.content.substring(0, 200)}...`
            : article.content;

        return (
          <Grid item xs={12} sm={6} md={3} key={article.id}>
            <Card className={classes.card} onClick={() => setCurrentArticle(article)}>
              <CardContent>
                <Typography gutterBottom variant="h5" component="h2">
                  {`Artículo ${article.number}`}
                </Typography>
                <Typography
                  variant="body1"
                  color="textSecondary"
                  component="p"
                  className={classes.cardContent}
                >
                  {contentPreview}
                </Typography>
                <Typography
                  variant="caption"
                  color="textSecondary"
                  component="p"
                  alignLeft
                  noWrap
                  className={classes.keywords}
                >
                  {`Palabras clave: ${article.keywords.join(', ')}`}
                </Typography>
              </CardContent>
              <CardActions>
                <Chip
                  size="small"
                  color="secondary"
                  label={`${article.minutesToRead} mins`}
                  className={classes.minutesToRead}
                />
              </CardActions>
            </Card>
          </Grid>
        );
      })}
      {currentArticle && (
        <Dialog
          maxWidth="sm"
          scroll="paper"
          onClose={() => setCurrentArticle(undefined)}
          open={currentArticle !== undefined}
        >
          <DialogTitle>{`Artículo ${currentArticle.number}`}</DialogTitle>
          <DialogContent dividers>
            <DialogContentText style={{ whiteSpace: 'pre-wrap' }}>
              {currentArticle.content}
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button
              variant="contained"
              autoFocus
              onClick={() => setCurrentArticle(undefined)}
              color="primary"
            >
              Ok
            </Button>
          </DialogActions>
        </Dialog>
      )}
    </Grid>
  );
};

export default ArticlesList;
