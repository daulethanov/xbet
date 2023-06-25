import React, { createContext, useState } from 'react';
import './App.css';
import { Route, Routes } from 'react-router-dom';
import Home from './pages/home/Home';
import Login from './pages/login/Login';
import PersonalArea from './pages/personal-area/PersonalArea';
import MatchPage from './pages/match-page/MatchPage';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import ClosedMatch from './pages/closed-match/ClosedMatch';
import ModalRent from './component/modal/modal-rent/ModalRent';
export const MyContext = createContext()


function App() {
	const [modalRentOpen, setModalRentOpen] = useState(false)
	const axiosInstance = axios.create({
		baseURL: 'http://127.0.0.1:5000/api/',
		headers: {
		  "Authorization": `Bearer ${localStorage.getItem("token")}`
		}
	  });
	const storedUserLogged = localStorage.getItem('userLogged') === 'true';
	const [userLogged, setUserLogged] = useState(storedUserLogged);

	return (
		<MyContext.Provider value={{
			userLogged,
			setUserLogged,
			axiosInstance,
			setModalRentOpen,
			modalRentOpen
		}}>
			<Routes>
				<Route path='/' element={<Home></Home>}></Route>
				<Route path='/login' element={<Login></Login>}></Route>
				<Route path='/personal-area' element={<PersonalArea></PersonalArea>}></Route>
				<Route path='/match-page' element={<MatchPage></MatchPage>}></Route>
				<Route path='/closed-match' element={<ClosedMatch></ClosedMatch>}></Route>
			</Routes>
		</MyContext.Provider>
	);
}

export default App;
