import React, { useState, useEffect } from 'react';
import './App.css';	

function App() {
	const [guess, setGuess] = useState("");
	const [letterData, setResult] = useState([]);
	const [isLoss, setIsLoss] = useState(false)
	const [isWin, setIsWin] = useState(false)
	const [isDisabled, setDisabled] = useState(false)
	const [gameId, setGameId] = useState("")


	useEffect(() => {
		const fetchData = async () => {
			console.log("hello")
		  const response = await fetch('http://127.0.0.1:5000/createGame');
		  if (response.ok) {
			const data = await response.json();
			console.log(data);
			setGameId(data.game)
		}}
		fetchData().catch(console.error);
	}, [])

	const handleGuess = async () => {
	  try {
		if (guess.length != 5){
			return
		}
		  console.log("Sending guess:", { guess });
		  const response = await fetch('http://127.0.0.1:5000/guess', {
			  method: 'POST',
			  headers: {
				  'Content-Type': 'application/json'
			  },
			  body: JSON.stringify({ guess: guess, gameId: gameId})
		  });

		  if (response.ok) {
			  const data = await response.json();
			  console.log(data);
			  let tempData = {
			  }
			  if (data.result.every(val=>val == "correct")){
				setIsWin(true)
				setDisabled(true)
			  }
			  else if (data.guessCount >= 5){
				console.log("hello")
				setIsLoss(true)
				setDisabled(true)
			  }
			  for (let i = 0; i < 5; i++) {
					tempData["l"+ i] = {"letter": guess.charAt(i),"result": data.result[i]}
				}
				setResult([
					...letterData,
					tempData
				])
				console.log(letterData)
			}
			  else {
			  console.error(`HTTP error! status: ${response.status}`);
			  
		  }


	  } catch (error) {
		  console.error("Error during the guess request", error);
	  }
  };
  
	return (
		<div className="App">
			<header className="App-header">
				<h1>Wordle</h1>
				<input
					type="text"
					value={guess}
					onChange={(e) => setGuess(e.target.value)}
					minLength={5}
					maxLength={5}
				/>
				<button disabled={isDisabled} onClick={handleGuess}>Submit Guess</button>	
				<table>{letterData.map(entry => (
					<tr>
						<td className={entry.l0.result}>{entry.l0.letter}</td>
						<td className={entry.l1.result}>{entry.l1.letter}</td>
						<td className={entry.l2.result}>{entry.l2.letter}</td>
						<td className={entry.l3.result}>{entry.l3.letter}</td>
						<td className={entry.l4.result}>{entry.l4.letter}</td>
					</tr>))}
				</table>
				{isWin? (
					<div>Win!</div>
				):(<div></div>)}				
				{isLoss? (
					<div>Loss</div>
				):(<div></div>)}
			</header>
		</div>
	);
}
export default App;
