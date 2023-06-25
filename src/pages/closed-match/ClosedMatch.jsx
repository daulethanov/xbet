import React, { useContext, useState, useEffect } from "react";
import "./closedMatch.css";
import Header from "../../component/header/Header";
import ModalCheck from "../../component/modal/modal-check/ModalCheck";
import { MyContext } from "../../App";
import ModalExpenses from "../../component/modal/modal-expenses/ModalExpenses";

function ClosedMatch() {
	const [inputClosedMatch, setInputClosedMatch] = useState("");
	const { axiosInstance } = useContext(MyContext);
	const [cardTeam, setCardTeam] = useState(null);
	const [modalCheckOpen, setModalCheckOpen] = useState(false);
	const [commandName, setCommandName] = useState("");
	const [teamOne, setTeamOne] = useState([]);
	const [teamTwo, setTeamTwo] = useState([]);
	const [modalExpensesOpen, setModalExpensesOpen] = useState(false)
  
	const submitTeamOne = () => {
	  const updatedCommandName = commandName === "command1" ? "command1" : "command2";
  
	  const submitTeamOneData = {
		name: updatedCommandName,
		users: [
		  {
			email: inputClosedMatch,
		  },
		],
	  };
  
	  axiosInstance.post("bet/command/create", submitTeamOneData);
	};
  
	const submitTeamTwo = () => {
	  const updatedCommandName = commandName === "command1" ? "command1" : "command2";
  
	  const submitTeamTwoData = {
		name: updatedCommandName,
		users: [
		  {
			email: inputClosedMatch,
		  },
		],
	  };
  
	  axiosInstance.post("bet/command/create", submitTeamTwoData);
	};
  
	useEffect(() => {
		const fetchData = async () => {
		  try {
			const res = await axiosInstance.get("bet/command/1");
			console.log(res.data); // Check the response data structure
			setTeamOne(res.data.users);
		  } catch (error) {
			console.error(error);
		  }
		};
		fetchData();
	  }, []);

	  useEffect(() => {
		const fetchData = async () => {
		  try {
			const res = await axiosInstance.get("bet/command/2");
			console.log(res.data); // Check the response data structure
			setTeamTwo(res.data.users);
		  } catch (error) {
			console.error(error);
		  }
		};
		fetchData();
	  }, []);
	  
  
	return (
	  <div>
		<ModalExpenses modalExpensesOpen={modalExpensesOpen} setModalExpensesOpen={setModalExpensesOpen}></ModalExpenses>
		<ModalCheck modalCheckOpen={modalCheckOpen} setModalCheckOpen={setModalCheckOpen}></ModalCheck>
		<Header></Header>
		<div className="closed__match">
		  <h2>Закрытый матч</h2>
		  <h3>Пригласить игроков</h3>
		  <div className="search__user">
			<div className="search__user__content">
			  <input
				value={inputClosedMatch}
				onChange={(e) => setInputClosedMatch(e.target.value)}
				type="text"
				placeholder="Введите почту"
			  />
			  <button value="command1" onClick={submitTeamOne}>
				Отправить команда 1
			  </button>
			  <button value="command2" onClick={submitTeamTwo}>
				Отправить команда 2
			  </button>
			</div>
		  </div>
		  <div className="closed__match__check">
			<div className="closed__match__check__content">
			  <div className="closed__match__check__check" onClick={() => setModalCheckOpen(true)}>
				<span>0:0</span>
			  </div>
			  <button onClick={() => setModalExpensesOpen(true)}>Расходы</button>
			  <div style={{ width: "500px", textAlign: "center" }}>
				<h4>Условия: Игра на интерес</h4>
				<h4>Место: Алиханова 24</h4>
			  </div>
			  <button>Начать матч</button>
			</div>
		  </div>
		  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: '100px' }}>
			<div className="team__one">
			  <div className="team__one__content">
				<div className="team__one__number">
				  Команда 1
				  <div></div>
				</div>
				{teamOne.length > 0 &&
  teamOne.map((obj) => (
    <div className="card__team" key={obj.id}>
      <img src="img/foto-user.jpg" alt="" />
      <h5 style={{ color: obj.active_math ? "green" : "red" }}>{obj.full_name ? obj.full_name : "No Name"}</h5>
    </div>
  ))}
			  </div>
			</div>
			<div className="team__lobbi">
			  <div className="team__lobbi__content">
				<div className="team__lobbi__txt">Лист ожидания</div>
			  </div>
			</div>
			<div className="team__two">
			  <div className="team__one__content">
				<div className="team__one__number">
				  Команда 2
				  <div></div>
				</div>
				{teamTwo.length > 0 &&
			teamTwo.map((obj) => (
				<div className="card__team" key={obj.id}>
				<img src="img/foto-user.jpg" alt="" />
				<h5 style={{ color: obj.active_math ? "green" : "red" }}>{obj.full_name ? obj.full_name : "No Name"}</h5>
				</div>
			))}
			  </div>
			</div>
		  </div>
		  {/* <h3>Ставки</h3>
		  <div className="rates">
			<div className="rates__content">
			  <ul>
				<li>Основные</li>
				<li>Поставленные ставки</li>
				<li className="active">Поставить ставку</li>
			  </ul>
			  <div style={{ padding: "0 30px" }}>
				<h3>Результаты игры</h3>
				<div className="rates__button">
				  <button>Команда 1</button>
				  <button>Ничья</button>
				  <button>Команда 2</button>
				</div>
			  </div>
			</div>
		  </div> */}
		</div>
	  </div>
	);
  }
  
  export default ClosedMatch;