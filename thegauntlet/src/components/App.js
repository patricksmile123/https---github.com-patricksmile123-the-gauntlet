import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Wordle from './Wordle';
import './App.css';
import Signup from './Signup';
import Login from './Login';



function App() {
	const [user, setUser] = useState({});
	useEffect(() => {console.log(user)}, [user]);
	return (
	  <Router>
		<Routes>
		  {!!(user.username) && <>
		  	<Route path="/wordle" element={<Wordle user={user} />} />
		  </>}
		  {!(user.username) && <>
		  	<Route path="/signup" element={<Signup user={user} />}/>
		  	<Route path="/login" element={<Login user={user} setUser={setUser}/>}/>
		  </>}
		  <Route path="*" element={<Navigate user={user} to={!!(user.username) ? "/wordle" : "/login"}/>} /> 
		</Routes>
	  </Router>
	);
  }

export default App;
