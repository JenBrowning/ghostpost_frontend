import React, { Component } from 'react';
import './App.css';
import { BrowserRouter as Router, Route} from "react-router-dom";

import Boasts from "./components/index.js"
import BoastFilter from "./components/boasts.js"
import RoastFilter from "./components/roasts.js"

class App extends Component {

  render() {
    return (
      <Router>
        <div>
        <Route path="/" exact component={Boasts} />
        <Route path="boasts" exact component={BoastFilter} />
        <Route path="roasts" exact component={RoastFilter} />
        </div>
      </Router>
    );
  }
}

export default App;
