import ReactDOM from 'react-dom';
import React, { Component } from 'react';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import Home from './Home';
import NegEx from './NegEx';

class App extends Component {
  render() {
    return (
      <Router>
        <div>
        	<nav className="navbar navbar-dark bg-dark">
					  <div className="container-fluid">
					    <div className="navbar-header">
					      <a className="navbar-brand" href="/">Applications</a>
					    </div>
					    <ul className="navbar-nav mr-auto">
					      <li className="nav-item"><a className="nav-link" href="/negex_implementation">Neg Ex</a></li>
					    </ul>
					  </div>
					</nav>
					<div className="appContainer">
	          <Switch>
	            <Route exact path='/' component={Home} />
	            <Route exact path='/negex_implementation' component={NegEx} />
	          </Switch>
          </div>
        </div>
      </Router>
    );
  }
}
export default App;
