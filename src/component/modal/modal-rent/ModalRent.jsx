import React, { useContext } from "react";
import './modalRent.css';
import { useState } from "react";
import { MyContext } from "../../../App";
import axios from "axios";

function ModalRent() {

	const {axiosInstance, modalRentOpen, setModalRentOpen} = useContext(MyContext)
	const [buttonChoice, setButtonChoice] = useState(true)
	

	const submitMatch = async () => {
		const dataMatch = {
		  name: "Футбольный клуб “ЖМЫХ”",
		  active_math: buttonChoice,
		  hall_ids: [1],
		  user_id: localStorage.getItem("id")
		};
	
		try {
		  await axiosInstance.post("bet/math/create/first", dataMatch);
		  setModalRentOpen(false);
		} catch (error) {
		  console.log(error);
		}
	  };


	return (
		<div className={modalRentOpen ? "modal__rent active" : "modal__rent"}>
			<div className="modal__rent__content">
				<div style={{ width: '385px' }}>
					<img src="img/foto13.jpg" alt="" />
					<h2>Футбольный клуб “ЖМЫХ”</h2>
					<h4>Описание клуба которое рассказывает о себе , во что возможно поиграть и тому подобное , главная задача описания такова</h4>
					<h3>Стоимость аренды поля: 10.000 Тг - час</h3>
				</div>
				<div style={{ width: '255px' }}>
					<h3 style={{ marginTop: '0' }}>Выберите время</h3>
					<div className="time"><img src="img/foto14.svg" alt="" /> 27 мая - 14:00-15:00</div>
					<button onClick={() => setButtonChoice(true)}>Закрытый матч <img src={buttonChoice === true ? "img/foto15.svg" : "img/foto16.svg"} alt="" /></button>
					<button onClick={() => setButtonChoice(false)}>Открытый матч <img src={buttonChoice === false ? "img/foto15.svg" : "img/foto16.svg"} alt="" /></button>
					<button onClick={() => submitMatch()} id="button__rent" style={{marginTop: '150px'}}>Арендовать</button>
					<button id="button__rent" onClick={() => setModalRentOpen(false)}>Отмена</button>
				</div>
			</div>
		</div>
	)

}

export default ModalRent