import React, { useContext, useEffect, useState } from "react";
import './home.css';
import Header from "../../component/header/Header";
import CardOpenMatches from "../../component/card/card-open-matches/CardOpenMatches";
import CardCategory from "../../component/card/card-category/CardCategory";
import { NavLink } from "react-router-dom";
import axios from "axios";
import ModalRent from "../../component/modal/modal-rent/ModalRent";
import { MyContext } from "../../App";

function Home() {

	const {axiosInstance, modalRentOpen, setModalRentOpen} = useContext(MyContext)
	const [CardMatches, setCardMatches] = useState([])

	useEffect(() => {
		const feacgData = async () => {
			const  res = await axiosInstance.get('bet/math/list')
			setCardMatches(res.data)
		}
		feacgData()
	}, [])

	return (
		<div className="home">
			<ModalRent></ModalRent>
			<Header></Header>
			<div className="home__width">
				<h2>Открытые матчи</h2>
				<div className="home__content">
					{CardMatches.map((Obj) => (
							<NavLink to={'/closed-match'}><CardOpenMatches key={Obj.id} {...Obj}></CardOpenMatches></NavLink>
					))}
				
				</div>
				<h2>Выбирай во что играть</h2>
				<div className="home__content">

					<CardCategory></CardCategory>
				</div>
				<h2>Топ-места</h2>
				<div className="home__content">
					<div className="top__places">
						<div className="top__places__content">
							<img src="img/foto3.jpg" alt="" />
							<div>
								<h2>Теннисный клуб Арын</h2>
								<h3>Стоимость: 12 000 ТНГ</h3>
								<h3>Открыто с 10:00 - 23:00 </h3>
								<button>Создать игру</button>
							</div>
						</div>
					</div>
					<div className="top__places">
						<div className="top__places__content">
							<img src="img/foto4.jpg" alt="" />
							<div>
								<h2>Баскетбол-Караганда</h2>
								<h3>Стоимость: 3 000 ТНГ</h3>
								<h3>Открыто с 10:00 - 23:00  </h3>
								<button>Создать игру</button>
							</div>
						</div>
					</div>
				</div>
				<h2>Последние добавленные друзья</h2>
				<div className="home__content">
					<img style={{ width: '133px', height: '133px', borderRadius: '10px' }} src="img/foto5.jpg" alt="" />
				</div>
				<div style={{ width: '100%', display: 'flex', justifyContent: 'center', gap: '20px' }}>
					<button onClick={() => setModalRentOpen(true)} id="create__match">Создать закрытый матч</button>
					<button id="create__match">Создать турнир</button>
				</div>
			</div>
		</div>
	)

}

export default Home;