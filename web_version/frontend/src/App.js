import React from 'react';
import './App.css';

function App() {
  const playerHand = ['Deal Breaker', 'Park Place', 'Money $5M'];
  const playerBank = ['$2M', '$3M'];
  const playerProperties = ['Boardwalk', 'Baltic Avenue'];

  return (
    <div className="app">
      <h1>Monopoly Deal UI</h1>
      
      <section className="hand">
        <h2>Your Hand</h2>
        <div className="cards">
          {playerHand.map((card, index) => (
            <div key={index} className="card">{card}</div>
          ))}
        </div>
      </section>

      <section className="bank">
        <h2>Your Bank</h2>
        <div className="cards">
          {playerBank.map((card, index) => (
            <div key={index} className="card">{card}</div>
          ))}
        </div>
      </section>

      <section className="properties">
        <h2>Your Properties</h2>
        <div className="cards">
          {playerProperties.map((prop, index) => (
            <div key={index} className="card">{prop}</div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default App;
