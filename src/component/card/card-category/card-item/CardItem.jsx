import React, {useContext, useEffect, useState} from "react";
import './cardItem.css';
import { MyContext } from "../../../../App";
import { NavLink } from "react-router-dom";

function CardItem() {
	const { axiosInstance } = useContext(MyContext);
	const [cardItems, setCardItems] = useState([]);
  
	useEffect(() => {
	  const fetchData = async () => {
		const res = await axiosInstance.get("bet/math/list");
		setCardItems(res.data);
	  };
	  fetchData();
	}, []);
  
	return (
	  <div>
		<NavLink to={'/closed-match'}>
			{cardItems.map((obj) => (
		  <div className="card__item__block" key={obj.id}>
			<div className="card__item ">
			  <img src="img/foto.jpg" alt="" />
			</div>
			<h2>{obj.name}</h2>
			{obj.hall.map((hall) => (
			  <h3 key={hall.id}>{hall.address}</h3>
			))}
		  </div>
		))}
		</NavLink>
		
	  </div>
	);
  }
  
  export default CardItem;
  