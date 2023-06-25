import React, { useContext, useEffect, useState } from "react";
import './personalArea.css';
import Header from "../../component/header/Header";
import CardOpenMatches from "../../component/card/card-open-matches/CardOpenMatches";
import axios from "axios";
import { MyContext } from "../../App";
import { NavLink } from "react-router-dom";
import ModalPayment from "../../component/modal/modal-payment/ModalPayment";

function PersonalArea() {

	const {axiosInstance} = useContext(MyContext)
	const [cardItems, setCardItems] = useState([]);
	const [modalPaymentOpen, setModalPaymentOpen] = useState(false)

	useEffect(() => {
		const feacgData = async () => {
			const  res = await axiosInstance.get('bet/math/list')
			setCardItems(res.data)
		}
		feacgData()
	}, [])

	

	const styleItem = [
		{
			title: 'Футбол',
			image: 'img/foto2.jpg'
		},
		{
			title: 'Бои',
			image: 'img/foto6.jpg'
		},
		{
			title: 'Хоккей',
			image: 'img/foto7.jpg'
		},
		{
			title: 'Баскетбол',
			image: 'img/foto8.jpg'
		},
		{
			title: 'Большой Теннис',
			image: 'img/foto9.jpg'
		}
	]

	return (
		<div>
			<ModalPayment modalPaymentOpen={modalPaymentOpen} setModalPaymentOpen={setModalPaymentOpen}></ModalPayment>
			<Header></Header>
			<div className="personal__area">
				<div style={{ width: '700px', display: 'flex', justifyContent: 'space-between' }}>
					<div>
						<img src="img/foto5.jpg" alt="" />
					</div>
					<div>
						<h3>ИМЯ:</h3>
						<h4 style={{ color: '#FF0606' }}>Феникс</h4>
						<h3>Любимая игра:</h3>
						<h4 style={{ color: '#C4F750' }}>Футбол</h4>
						<h3>Возвраст:</h3>
						<h4 style={{ color: '#C4F750' }}>20 лет</h4>
					</div>
					<div>
						<h3>Контакты:</h3>
						<h4 style={{ color: '#FF0606' }}>877782788</h4>
						<h3 onClick={() => setModalPaymentOpen(true)} style={{cursor: 'pointer'}}>Оплата:</h3>
						<h4 style={{ color: 'white' }}>4402********6655</h4>
					</div>
				</div>
				<h5>Изменить</h5>
				<div className="personal__area__line"></div>
				<h2>Последние сыгранные матчи</h2>
       <NavLink to={'/closed-match'}>
	   {cardItems.map((obj) => (
          <CardOpenMatches key={obj.id} name={obj.name} start_math={obj.start_math} />
        ))}
	   </NavLink>
				<h2 style={{ marginTop: '25px' }}>Выберите оформление личного кабинета</h2>
				<ul className="style__item">
					{styleItem.map((Obj) => (
							<li><img src={Obj.image}></img>{Obj.title}</li>
					))}
				</ul>
			</div>
		</div>
	)

}

export default PersonalArea;