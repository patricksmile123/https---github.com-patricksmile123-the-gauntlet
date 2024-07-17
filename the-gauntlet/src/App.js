import React, { useState } from 'react';
import './App.css';

function App() {
    const [guess, setGuess] = useState("");
    const [result, setResult] = useState([]);

    const handleGuess = async () => {
      try {
          console.log("Sending guess:", { guess });

          const response = await fetch('http://127.0.0.1:5000/guess', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ guess: guess })
          });

          if (response.ok) {
              const data = await response.json();
              console.log(data);
          } else {
              console.error(`HTTP error! status: ${response.status}`);
          }
          
          setResult(response.data.result);
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
                    maxLength={5}
                />
                <button onClick={handleGuess}>Submit Guess</button>
                <div>
                    {result.map((res, index) => (
                        <span key={index} className={res}>{guess[index]}</span>
                    ))}
                </div>
            </header>
        </div>
    );
}

export default App;
