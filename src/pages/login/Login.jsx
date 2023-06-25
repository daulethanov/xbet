import React, { useContext, useState, useEffect } from 'react';
import './login.css';
import { MyContext } from '../../App';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Login() {
	const { setUserLogged, axiosInstance } = useContext(MyContext);
	const navigate = useNavigate();
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [emailReg, setEmailReg] = useState('');
	const [passwordReg, setPasswordReg] = useState('');
	const [fullName, setFullName] = useState('');

	useEffect(() => {
		const storedUserLogged = localStorage.getItem('userLogged');
		if (storedUserLogged) {
			setUserLogged(JSON.parse(storedUserLogged));
		}
	}, []);

	const registrLogin = async (e) => {
		e.preventDefault();

		const dataReg = {
			email: emailReg,
			password: passwordReg,
			full_name: fullName,
		};

		try {
			const response = await axiosInstance.post(`auth/register`, dataReg);
			setEmailReg('');
			setPasswordReg('');
			setFullName('');
			navigate('/');
			setUserLogged(true);
			localStorage.setItem('userLogged', JSON.stringify(true));
			localStorage.setItem('token', response.data.access_token);
		} catch (error) {
			console.log('Registration error:', error);
		}
	};

	
	const authLogin = async (e) => {
		e.preventDefault();

		const dataReg = {
			email: email,
			password: password
		};

		try {
			const response = await axiosInstance.post(`auth/login`, dataReg);
			setEmailReg('');
			setPasswordReg('');
			setFullName('');
			navigate('/');
			setUserLogged(true);
			localStorage.setItem('userLogged', JSON.stringify(true));
			localStorage.setItem('token', response.data.access_token);
		} catch (error) {
			console.log('Registration error:', error);
		}
	};

	return (
		<div className="login">
			<div style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
				<form onSubmit={registrLogin}>
					<div className="form__content">
						<h2>Регистрация</h2>
						<div className="form__content__line"></div>
						<div style={{ position: 'relative', marginBottom: '22px' }}>
							<h5>Gmail почта</h5>
							<input
								type="email"
								value={emailReg}
								onChange={e => setEmailReg(e.target.value)} />
						</div>
						<div style={{ position: 'relative', marginBottom: '22px' }}>
							<h5>Пароль</h5>
							<input
								type="password"
								value={passwordReg}
								onChange={e => setPasswordReg(e.target.value)} />
						</div>
						<div style={{ position: 'relative', marginBottom: '22px' }}>
							<h5>Ф.И.О.</h5>
							<input type="text"
								value={fullName}
								onChange={e => setFullName(e.target.value)} />
						</div>
						<button type="submit">Зарегестрироваться</button>
					</div>
				</form>
				<form onSubmit={authLogin}>
					<div className="form__content">
						<h2>Авторизация</h2>
						<div className="form__content__line"></div>
						<div style={{ position: 'relative', marginBottom: '22px' }}>
							<h5>Gmail почта</h5>
							<input
								type="email"
								value={email}
								onChange={e => setEmail(e.target.value)} />
						</div>
						<div style={{ position: 'relative', marginBottom: '22px' }}>
							<h5>Пароль</h5>
							<input type="password"
								value={password}
								onChange={e => setPassword(e.target.value)} />
						</div>
						<button type='submit'>Вход</button>
					</div>
				</form>
			</div>
		</div>
	)

}

export default Login;