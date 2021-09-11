/**
 * 
 * Author: yueying chang
 * Student id: 1183384
 * Team: COMP90024 - team 24
 */

import './App.css';
import Sidebar from './components/Sidebar'
import React from "react";
import { Router, Switch, Route } from "react-router-dom";

import Analysis from "./pages/Analysis";
import Home from "./pages/Home";
import history from './history';
class App extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      scenario: null
    }
  }

  callbackFunction = (childData) => {
    this.setState({
      scenario: childData.scenario,
      language: childData.language,
    })
  };

  render(){
  return (
    <div>
      <Sidebar parentCallback = {this.callbackFunction}/>
      <Router history={history}>
                <Switch>
                    <Route path="/" exact render={(props) => <Home globalStore={{scenario: this.state.scenario, language: this.state.language}} {...props} /> } />
                    <Route path="/Analysis" component={Analysis} />
                </Switch>
            </Router>
    </div>
  );
  }
}

export default App;
