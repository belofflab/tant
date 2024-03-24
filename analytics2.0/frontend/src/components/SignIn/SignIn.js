import React, { useEffect, useState } from 'react';

import {
    Avatar, Button, TextField,
    FormControlLabel, Checkbox, Link,
    Grid, Box, Typography, Container, CircularProgress
} from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';

import Copyright from '../Copyright';
import CloseIcon from '@mui/icons-material/Close';
import { useDispatch, useSelector } from 'react-redux'
import { userLogin } from '../../store/auth/auth.actions'



export default function SignIn({ onRegisterClick, handleModal }) {

    const [customError, setCustomError] = useState('');

    const { success, loading, error } = useSelector((state) => state.auth)

    const dispatch = useDispatch();
    useEffect(() => {
        if (success) {
            handleModal(false);
        }
        if (error) {
            setCustomError(error);
        }
    }, [setCustomError, success, error, handleModal])


    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);

        // const idx = data.get('idx');
        const password = data.get('password');

        if (!password.length) {
            setCustomError('Пожалуйста введите пароль')
            return;
        }


        dispatch(userLogin({ idx: data.get('idx'), password: data.get('password') }))

    };

    return (

        <Container component="main">
            <Box sx={{display: 'flex', justifyContent: 'end'}}>
                <CloseIcon sx={{cursor: 'pointer'}} onClick={() => handleModal(false)}/>
            </Box>
            <Box
                sx={{
                    marginTop: 4,
                }}
            >
                {loading ? (
                    <CircularProgress />
                ) : (
                    <Box sx={{
                        textAlign: '-webkit-center',
                        alignItems: 'center'
                    }}>
                        <Avatar sx={{ m: 1, bgcolor: '#c764d0' }}>
                            <LockOutlinedIcon />
                        </Avatar>
                        <Typography component="h1" variant="h5">
                            Авторизация
                        </Typography>
                        <Typography component="span" variant="caption" sx={{ color: 'red' }}>
                            {customError}
                        </Typography>
                        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                id="idx"
                                label="ID пользователя Telegram"
                                name="idx"
                                autoFocus
                            />
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                name="password"
                                label="Пароль"
                                type="password"
                                id="password"
                                autoComplete="current-password"
                            />
                            <FormControlLabel
                                control={<Checkbox value="remember" sx={{color: '#c764d0'}} />}
                                label="Оставаться в системе"
                            />
                            <Button
                                type="submit"
                                fullWidth
                                variant="contained"
                                sx={{ mt: 3, mb: 2, backgroundColor: '#c764d0' }}
                            >
                                Войти
                            </Button>
                            <Grid container>
                                <Grid item xs>
                                    <Link href="#" variant="body2" sx={{color: '#c764d0'}}>
                                        Забыли пароль?
                                    </Link>
                                </Grid>
                                <Grid item>
                                    <Link sx={{color: '#c764d0'}} onClick={() => onRegisterClick(false)} href="#" variant="body2">
                                        {"Ещё не зарегистрированы? "}
                                    </Link>
                                </Grid>
                            </Grid>
                        </Box>
                    </Box>
                )}
            </Box>
            <Copyright sx={{ mt: 8, mb: 4 }} />
        </Container>
    );
}