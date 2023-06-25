import React, { useContext, useState } from "react";
import "./closedMatch.css";
import Header from "../../component/header/Header";
import ModalCheck from "../../component/modal/modal-check/ModalCheck";
import { MyContext } from "../../App";



	function ClosedMatch() {
		const [inputClosedMatch, setInputClosedMatch] = useState('');
		const { axiosInstance } = useContext(MyContext);
		const [cardTeam, setCardTeam] = useState(null);
		const [modalCheckOpen, setModalCheckOpen] = useState(false);
		const [commandName, setCommandName] = useState('');
		const [teamOne, setTeamOne] = useState([])
	  
		function dragStartHandler(e) {
		  e.dataTransfer.setData("text/plain", e.target.id);
		}
	  
		function dragEnterHandler(e) {
		  e.preventDefault();
		  e.target.style.background = "#00ff87";
		}
	  
		function dragLeaveHandler(e) {
		  e.target.style.background = "black";
		}
	  
		function dragOverHandler(e) {
		  e.preventDefault();
		}
	  
		function dropHandler(e, team) {
		  e.preventDefault();
		  const cardId = e.dataTransfer.getData("text/plain");
		  const card = document.getElementById(cardId);
	  
		  if (card) {
			e.target.appendChild(card);
			setCardTeam(team);
			e.target.style.background = "black";
		  }
		}
	  
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
			const feacgData = async () => {
				const  res = await axiosInstance.get('bet/command/1')
				setTeamOne(res.data)
			}
			feacgData()
		}, [])
	  
	return (
		<div>
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
						<button>Расходы</button>
						<div style={{ width: "500px", textAlign: "center" }}>
							<h4>Условия: Игра на интерес</h4>
							<h4>Место: Алиханова 24</h4>
						</div>
						<button>Начать матч</button>
					</div>
				</div>
				<div style={{ display: "flex", justifyContent: "space-between" }}>
					<div
						className="team__one"
						onDragOver={dragOverHandler}
						onDrop={(e) => dropHandler(e, "team__one")}
					>
						<div className="team__one__content">
							<div className="team__one__number">
								Команда 1
								<div>
								</div>
								
							</div>
							<div className="card__team ">
								<img src="img/foto-user.jpg" alt="" />
									<h5>Руслан</h5>
							</div>
							
							
						</div>
					</div>
					<div className="team__lobbi">
						<div className="team__lobbi__content">
							<div className="team__lobbi__txt">Лист ожидания</div>
							

						</div>
					</div>
					<div
						className="team__two"
						onDragOver={dragOverHandler}
						onDrop={(e) => dropHandler(e, "team__two")}
					>
						<div className="team__one__content">
							<div className="team__one__number">
								Команда 2
								<div>
								</div>
								
							</div>
							<div className="card__team ">
								<img src="img/foto-user.jpg" alt="" />
									<h5>Руслан</h5>
							</div>
							
							
						</div>
					</div>
				</div>
				<h3>Ставки</h3>
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
				</div>
			</div>
		</div>
	);
}

export default ClosedMatch;