import React from 'react';
import ApolloClient from 'apollo-boost' 
import { ApolloProvider } from '@apollo/react-hooks' 

import Countries from './pages/countries/countries'
import CountryDetail from './pages/countries/country-detail/country-detail'

import 'bootstrap/dist/css/bootstrap.min.css' 

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom" 

const client = new ApolloClient({
  uri: 'http://127.0.0.1:5000/graphql'
})

const App = () => (
  <ApolloProvider client = {client} style = {{ margin: 0 }}>
    <div className = 'container-fluid'
      style = {{
        backgroundColor: 'whitesmoke',
        minHeight: 800,
        padding: 0
      }}
    >
      <div className = 'container-fluid bg-dark'>
        <header className = 'bg-dark align-items-center'>
          <div className = "row">
            <div className = "col-sm-4">

            </div>
            <div className = "col-sm-4">
              <h1 
                style = {{
                  fontWeight: 0.5,
                  fontSize: '4.0em',
                  paddingBottom: 40,
                  marginLeft: 100,
                  margin: 'auto',
                  color: '#FF4136'
                }}
                className = 'bg-dark text-center'
              >
                Don't Panic!
              </h1>
            </div>
            <div className = "col-sm-4">

            </div>
          </div>
        </header>
      </div>
      <Router>
        <Switch>
          <Route path = '/' exact component={Countries} />
          <Route
          path = '/country/:countryId' 
          exact component={CountryDetail}
          
          />
        </Switch>
      </Router>
    </div>
  </ApolloProvider>
)

export default App;
