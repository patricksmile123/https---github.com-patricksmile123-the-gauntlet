import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Wordle from './Wordle';
import './App.css';
import Signup from './Signup';

function App() {
	return (
	  <Router>
		<Routes>
		  <Route path="/" element={<Wordle />} />
		  <Route path="/signup" element={<Signup />}/>
		</Routes>
	  </Router>
	);
  }

export default App;
