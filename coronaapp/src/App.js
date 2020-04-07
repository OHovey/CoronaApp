import React from "react";
import ApolloClient, { gql } from "apollo-boost";
import { ApolloProvider } from "@apollo/react-hooks";

import Countries from "./pages/countries/countries";
import CountryDetail from "./pages/countries/country-detail/country-detail";
import DatabaseDetail from "./includes/header";

import "bootstrap/dist/css/bootstrap.min.css";

import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

const client = new ApolloClient({
  uri: "http://127.0.0.1:5000/graphql",
});

const GET_DATABASE_UPDATE = gql`
  {
    allUpdates(first: 1) {
      edges {
        node {
          date
        }
      }
    }
  }
`;

const App = () => (
  <ApolloProvider client={client} style={{ margin: 0 }}>
    <div
      className="container-fluid"
      style={{
        backgroundColor: "whitesmoke",
        minHeight: 1200,
        padding: 0,
        backgroundColor: '#bfbfbf'
      }}
    >
      <div className="container-fluid bg-dark">
        <header className="bg-dark align-items-center">
          <div className="row">
            <div className="col-sm-3"></div>
            <div className="col-sm-6">
              <h1
                style={{
                  fontWeight: 100,
                  fontSize: "6.0em",
                  marginLeft: 100,
                  margin: "auto",
                  color: "#a89b9b",
                }}
                className="bg-dark text-center"
              >
                <span style = {{ color: '#ff5757' }}>F </span> 
                <span style = {{ color: "#ff6e6e" }}>l </span>
                <span style = {{ color: "#ff9191" }}>u </span> 
                <span style = {{ color: '#943a3a' }}>B </span> 
                <span style = {{ color: '#945050' }}>r </span> 
                <span style = {{ color: '#8f6060' }}>o </span> 
              </h1>
              <p className = "text-center" style = {{ color: '#ff9191', fontWeight: 100, marginTop: 10 }}>A Covid-19 Info Site</p>
              {/* <hr style = {{ backgroundColor: '#8f6060' }} />  */}
            </div>
            <div className="col-sm-3">
              <DatabaseDetail />
            </div>
          </div>
        </header>
      </div>
      <Router>
        <Switch>
          <Route path="/" exact component={Countries} />
          <Route path="/country/:countryId" exact component={CountryDetail} />
        </Switch>
      </Router>
    </div>
  </ApolloProvider>
);

export default App;
