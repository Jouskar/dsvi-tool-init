import React, { useState } from 'react';
import useHttp, { endpoints } from '../hooks/use-http';
import { useForm, Controller } from "react-hook-form";
import { TextField, Box ,
  PropTypes,
  Avatar,
  Button,
  CssBaseline,
  FormControl,
  FormControlLabel,
  Checkbox,
  Input,
  InputLabel,
  Paper,
  Typography,

} from '@mui/material';
import { LockOutlined } from '@mui/icons-material';
import { withStyles } from '@mui/material';

const Login = () => {
  const styles = theme => ({
    main: {
      width: 'auto',
      display: 'block', // Fix IE 11 issue.
      marginLeft: theme.spacing.unit * 3,
      marginRight: theme.spacing.unit * 3,
      [theme.breakpoints.up(400 + theme.spacing.unit * 3 * 2)]: {
        width: 400,
        marginLeft: 'auto',
        marginRight: 'auto',
      },
    },
    paper: {
      marginTop: theme.spacing.unit * 8,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: `${theme.spacing.unit * 2}px ${theme.spacing.unit * 3}px ${theme.spacing.unit * 3}px`,
    },
    avatar: {
      margin: theme.spacing.unit,
      backgroundColor: theme.palette.secondary.main,
    },
    form: {
      width: '100%', // Fix IE 11 issue.
      marginTop: theme.spacing.unit,
    },
    submit: {
      marginTop: theme.spacing.unit * 3,
    },
  });

  const { control, handleSubmit } = useForm({
    defaultValues: {
      username: '',
      password: '',
    }
  });

  const requestConfigLogin = {
    method: 'POST',
    endpoint: endpoints.login,
    body: {
      username: '',
      password: '',
    }
  }

  const onSubmit = data => {
    console.log(data);
    setReqBody(data);

    fetchLogin();
  }

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const parseLoginData = (data) => {
    console.log(data);
  };

  const {isLoading, error, sendRequest: fetchLogin, setReqBody} = useHttp(requestConfigLogin, parseLoginData);

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
      >
          <Controller
            name="username"
            control={control}
            render={({ field }) => <TextField
              label="Username"
              {...field} />}
          />
          <Controller
            name="password"
            control={control}
            render={({ field }) => <TextField
              label="Password"
              type='password'
              {...field}
            />}
          />
          <Button variant='contained' color='primary' type="submit">Login</Button>
      </Box>
    </form>
  );
};

export default Login;

/*
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={handleUsernameChange}
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={handlePasswordChange}
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div> */