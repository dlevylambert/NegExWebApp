import ReactDOM from 'react-dom';
import React, { Component } from 'react';
import { BrowserRouter as Router, Switch, Route, Link, withRouter } from 'react-router-dom';
import axios from 'axios';
import Home from './Home';
import NegEx from './NegEx';
import Login from './Login';

class App extends Component {

  constructor(props) {
    super(props);
    this.state ={
      loggedIn:false,
    };
    axios.get('/is-logged-in').then(function(response){
      if (response.data.logged_in) {
        this.setState({loggedIn: true});
      }
      else {
        this.setState({loggedIn: false});
      }
    }.bind(this));
  }

  componentDidUpdate(prevProps) {
    if (this.props.location !== prevProps.location) {
      console.log("ROUTE CHANGES")
      axios.get('/is-logged-in').then(function(response){
        if (response.data.logged_in) {
          this.setState({loggedIn: true});
        }
        else {
          this.setState({loggedIn: false});
        }
      }.bind(this));
    }
  }

  render() {
    let loginOrLogoutComponent;
    if (this.state.loggedIn) {
      loginOrLogoutComponent = <li className="nav-item"><a className="nav-link" href="/logout">Logout</a></li>;
    }
    else {
      loginOrLogoutComponent = <li className="nav-item"><a className="nav-link" href="/login">Login</a></li>;
    }
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
					<ul className="nav navbar-nav navbar-right">
            {loginOrLogoutComponent}
					</ul>
				</div>
			</nav>
			<div className="appContainer">
        <Switch>
          <Route exact path='/' component={Home} />
		      <Route exact path='/negex_implementation' component={NegEx} />
		      <Route exact path='/login' component={Login} />
		    </Switch>
    	</div>
      </div>
    </Router>
    );
  }
}
export default App;
