import React, { useState } from 'react';
import './App.css';
import GameContainer from './GameContainer';
import RulesContainer from './RulesContainer'
import CheckersContainer from './CheckersContainer'

function App() {
  const [showRules, setShowRules] = useState(false)
  const [game, setGame] = useState(false)

  return (
    <div>
      <header><h1 id='header'>Checkers Minds</h1></header>
      {!game && !showRules && <GameContainer setShowRules={setShowRules} setGame={setGame} />}
      {!game && showRules && <RulesContainer setShowRules={setShowRules} />}
      {game && <CheckersContainer game={game} setGame={setGame} />}
    </div>
  );
}

export default App;
