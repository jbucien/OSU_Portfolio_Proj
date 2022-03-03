import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import CreateExercisePage from './pages/CreateExercisePage';
import EditExercisePage from './pages/EditExercisePage';
import { useState } from 'react';
import Navigation from './components/Navigation';
import { GiWeightLiftingUp } from "react-icons/gi";

function App() {

  //create new state variable so we can pass it down to HomePage and EditPage
  const [exerciseToEdit, setExerciseToEdit] = useState();

  return (
    <div className="App">
      <Router>
        <body>
          <header className="App-header">
            <div className="App-title-box">
              <h1 className="App-title">
                <GiWeightLiftingUp />
                Exercise Tracker
                <GiWeightLiftingUp />
              </h1>
              <p className="App-description">Keep track of your gains!</p>
            </div>
            <Navigation />
          </header>
          <main>
            <div>
                <Route path="/" exact>
                  <HomePage setExerciseToEdit={setExerciseToEdit} />
                </Route>
                <Route path="/create-exercise">
                  <CreateExercisePage />
                </Route>
                <Route path="/edit-exercise">
                  <EditExercisePage exerciseToEdit={exerciseToEdit} />
                </Route>
              </div>
          </main>
          <footer>
              <p>Jenna Bucien &copy; 2022</p>
            </footer>
        </body>
      </Router>      
    </div>
  );
}

export default App;
