import React, { useState } from "react";
import './matchPage.css';
import Header from "../../component/header/Header";
import CardItem from "../../component/card/card-category/card-item/CardItem";

function MatchPage() {

	const [selectItemActive, setSelectItemActive] = useState(0);
	const [selectOpen, setSelectOpen] = useState(false)

	const selectItem = [
		'Категория',
		'Футбол',
		'Бои',
		'Хоккей',
		'Баскетбол',
		'Большой Теннис',
		'Теннис',
		'Пейнтбол',
		'Волейбол'
	]

	const activeSelectItem = (index) => {
		setSelectOpen(false)
		setSelectItemActive(index)
	}

	return (
		<div>
			<Header></Header>
			<div className="match__page">
				<h2>Залы в Караганде</h2>
				<div style={{display: 'flex', gap: '15px'}}>
					<div style={{ position: 'relative' }}>
						<input type="text" placeholder="Поиск" name="" id="" />
						<img id="search__img" src="img/search.svg" alt="" />
					</div>
					<div className="select">
						<span onClick={() => setSelectOpen(!selectOpen)}>{selectItem[selectItemActive]}<img src="img/arrow.svg"></img></span>
						<ul className={selectOpen ? "active" : ''} >
							{selectItem.map((Obj, index) => (
								<li onClick={() => activeSelectItem(index)} className={selectItemActive === index ? "active" : ''}>{Obj}</li>
							))}
						</ul>
					</div>
				</div>
				<div style={{display: 'flex', flexWrap: 'wrap', gap: '30px', marginTop: '30px'}}>
					<CardItem></CardItem>
				</div>
			</div>
		</div>
	)
}

export default MatchPage;