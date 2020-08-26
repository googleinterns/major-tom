import { makeStyles } from '@material-ui/core/styles'

const styles = makeStyles(theme => ({
  card: {
    width: '100%',
    marginTop: 20,
    '&:hover': {
      backgroundColor: '#fafafa'
    },
    [theme.breakpoints.up('sm')]: {
      width: '70%'
    }
  },
  cardContent: {
    whiteSpace: 'pre-wrap',
    marginBottom: 15
  },
  resultsChip: {
    margin: '0px 0px 15px 5px'
  }
}))

export default styles
