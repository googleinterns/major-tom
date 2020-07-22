import { fade, makeStyles } from '@material-ui/core/styles';

const styles = makeStyles((theme) => ({
  appbar: {
    margin: '25px 0px',
  },
  root: {
    flexGrow: 1,
  },
  search: {
    position: 'relative',
    borderRadius: theme.shape.borderRadius,
    backgroundColor: fade(theme.palette.common.white, 0.15),
    '&:hover': {
      backgroundColor: fade(theme.palette.common.white, 0.25),
    },
    marginLeft: 0,
    width: '100%',
  },
  avatar: {
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
  },
  inputRoot: {
    color: 'inherit',
  },
  inputInput: {
    transition: theme.transitions.create('width'),
    width: '100%',
    fontWeight: 'bold',
    [theme.breakpoints.up('sm')]: {
      width: '35ch',
      '&:focus': {
        width: '45ch',
      },
    },
  },
}));

export default styles;
