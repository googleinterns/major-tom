import { makeStyles } from '@material-ui/core/styles'

const styles = makeStyles(() => ({
  card: {
    '&:hover': {
      cursor: 'pointer',
      backgroundColor: '#fafafa'
    }
  },
  cardContent: {
    whiteSpace: 'pre-wrap',
    marginBottom: 15
  }
}))

export default styles
