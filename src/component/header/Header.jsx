import React, { useState, useEffect, useContext } from "react";
import './header.css';
import { NavLink, useNavigate, useLocation } from "react-router-dom";
import { MyContext } from "../../App";


function Header() {

	const { userLogged, setUserLogged } = useContext(MyContext);
	const navigate = useNavigate();
	const [linlActive, setLinckActive] = useState(0);
	const location = useLocation();

	useEffect(() => {

		const isMatchPage = location.pathname === "/match-page";
		const isPersonalArea = location.pathname === "/personal-area";
		const isClosedMatch = location.pathname === "/closed-match";

		if (isMatchPage) {
			setLinckActive(null);
		} if (isPersonalArea) {
			setLinckActive(null);
		} if (isClosedMatch) {
			setLinckActive(null);
		}
	}, []);

	const headerItem = [{
		title: 'Главная',
		link: '/'
	},
	{
		title: 'Открытые матчи',
		link: '/d'
	},
	{
		title: 'Игры',
		link: '/1'
	},
	{
		title: 'Места',
		link: '/2'
	}
	]

	const outButton = () => {
		setUserLogged(false);
		localStorage.removeItem('token');
		navigate('/login');
	}

	return (
		<header>
			<div className="header__content">
				<NavLink to={'/'}><h1>Тматч</h1></NavLink>
				<ul>
					{headerItem.map((Obj, index) => (
						<li key={index}><NavLink onClick={() => setLinckActive(index)} to={Obj.link} className={linlActive === index ? "active__linck active" : "active__linck"}>{Obj.title}</NavLink></li>
					))}
				</ul>
				<div style={{
					fontSize: '16px',
					fontWeight: '600',
					lineHeight: '32px'
				}}>
					{userLogged ? (
						location.pathname === '/personal-area' ? (
							<span onClick={outButton}>Выход</span>
						) : (
							<NavLink to={'/personal-area'}>Личный кабинет</NavLink>
						)
					) : (
						<NavLink to={'/login'}>
							<span>Регистрация</span> / <span>Вход</span>
						</NavLink>
					)}
				</div>
			</div>
		</header>
	)

}

export default Header;