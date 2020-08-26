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
    marginBottom: 15,
    maxHeight: '20vh'
  }
}))

export default styles
