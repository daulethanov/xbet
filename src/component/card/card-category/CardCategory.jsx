import React from "react";
import './cardCategory.css';
import { NavLink } from "react-router-dom";

function CardCategory() {

	const categoryItem = [
		{
			title: 'Футбол',
			image: 'img/foto2.jpg',
			link: 'match-page'
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
		},
		{
			title: 'Теннис',
			image: 'img/foto10.jpg'
		},
		{
			title: 'Пейнтбол',
			image: 'img/foto11.jpg'
		},
		{
			title: 'Волейбол',
			image: 'img/foto12.jpg'
		}
	]

	return (
		<div className="card__category">
			<ul className="category__item">
				{categoryItem.map((Obj) => (
					<li><NavLink to={Obj.link}><img src={Obj.image}></img>{Obj.title}</NavLink></li>
				))}
			</ul>
		</div>
	)

}

export default CardCategory;