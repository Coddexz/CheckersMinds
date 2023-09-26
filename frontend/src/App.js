import React, { useState } from 'react';
import './App.css';
import GameContainer from './GameContainer';
import RulesContainer from './RulesContainer'

function App() {
  const [showRules, setShowRules] = useState(false)

  return (
    <div>
      <header><h1 id='header'>Checkers Minds</h1></header>
      {!showRules && <GameContainer setShowRules={setShowRules} />}
      {showRules && <RulesContainer setShowRules={setShowRules} />}
    </div>
  );
}

export default App;
