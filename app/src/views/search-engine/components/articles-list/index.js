import React, { useState } from 'react'
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
  Button
} from '@material-ui/core'
import styles from './styles'
import { DEFAULT_ARTICLE_PREVIEW_SIZE } from 'utils/constants'

const ArticlesList = ({ articles }) => {
  const [currentArticle, setCurrentArticle] = useState(undefined)
  const classes = styles()

  return (
    <Grid container spacing={3}>
      {articles.map((article) => {
        const contentPreview =
          article.content.length > DEFAULT_ARTICLE_PREVIEW_SIZE
            ? `${article.content.substring(0, DEFAULT_ARTICLE_PREVIEW_SIZE)}...`
            : article.content

        return (
          <Grid item xs={12} sm={6} md={3} key={article.id}>
            <Card className={classes.card} onClick={() => setCurrentArticle(article)}>
              <CardContent>
                <Typography gutterBottom variant='h5' component='h2'>
                  {`Artículo ${article.number}`}
                </Typography>
                <Typography
                  variant='body1'
                  color='textSecondary'
                  component='p'
                  className={classes.cardContent}
                >
                  {contentPreview}
                </Typography>
                <Typography
                  variant='caption'
                  color='textSecondary'
                  component='p'
                  noWrap
                  className={classes.keywords}
                >
                  {`Palabras clave: ${article.keywords.join(', ')}`}
                </Typography>
              </CardContent>
              <CardActions>
                <Chip
                  size='small'
                  color='secondary'
                  label={`${article.minutesToRead} mins`}
                  className={classes.minutesToRead}
                />
              </CardActions>
            </Card>
          </Grid>
        )
      })}
      {currentArticle && (
        <Dialog
          maxWidth='sm'
          scroll='paper'
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
              variant='contained'
              onClick={() => setCurrentArticle(undefined)}
              color='primary'
            >
              Ok
            </Button>
          </DialogActions>
        </Dialog>
      )}
    </Grid>
  )
}

export default ArticlesList
