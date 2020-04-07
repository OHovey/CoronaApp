import React, { useState } from 'react' 
import { gql } from 'apollo-boost' 
import { useQuery } from '@apollo/react-hooks' 
import { useHistory } from "react-router-dom"

import CountryDetailPage from './country-detail/country-detail'  

import 'bootstrap/dist/css/bootstrap.min.css' 

const GET_COUNTRIES = gql`
    {
        allCountries {
            edges {
              node {
                id 
                name 
                totalCases 
                totalDeaths
                history(first: 1) {
                    edges {
                        node {
                            newCases 
                            newDeaths
                        }
                    }
                }
              }
            }
          }
    }
`;

const searchCountries = (arr, text) => arr.filter(item => item.node.name.toLowerCase().includes(text))

function sortCountriesByInfectedCount(a, b) {
    if (a.node.totalCases < b.node.totalCases) return 1 
    if (b.node.totalCases < a.node.totalCases) return -1 

    return 0;
}

export default function Countries() {
    
    const { loading, error, data } = useQuery(GET_COUNTRIES)
    const [displayData,  setDisplayData] = useState([])

    let history = useHistory()

    // console.log('data: ' + data)

    if (loading) return <p>Loading...</p>

    if (data.allCountries.edges.length == 0) return <p>Could not retrieve data... probably updating, try again in a few seconds</p>

    data.allCountries.edges.sort(sortCountriesByInfectedCount)

    function sumCases(arr, key) {
        return arr.reduce((a, b) => a + (b.node[key] || 0), 0);
    }
    
    let totalCases = sumCases(data.allCountries.edges, 'totalCases')
    let totalDeaths = sumCases(data.allCountries.edges, 'totalDeaths')

    function passCountryToDetailPage(countryId) {
        history.push('/country/' + countryId)
    }

    let dataToDisplay = {}
    if (displayData.length == 0) {
        // console.log('yep its null')
        dataToDisplay = data.allCountries.edges
    } else {
        dataToDisplay = displayData
    }

    // console.log('dataToDisplay: ' + dataToDisplay)

    function alterDisplayData(text) {
        let comparisonData = data.allCountries.edges
        let filteredCountries = searchCountries(comparisonData, text) 
        console.log('filtered_countries: ' + filteredCountries)
        setDisplayData(filteredCountries)
    }


    return (
        <div className = 'container-fluid' style = {{ backgroundColor: '#bfbfbf' }}>
            <div className = "row bg-dark">
                <div className = "col-md-3 mx-auto">
                </div>
                <div className = "col-md-3 align-middle">
                    <p style = {{ fontSize: 28, color: '#b0b0b0', fontWeight: 100 }} className = "text-center">Global Cases: <span style = {{ color: '#ff5757', fontSize: 35 }}>{totalCases.toLocaleString()}</span></p>
                </div>
                <div className = "col-md-3 mg-auto">
                    <p style = {{ fontSize: 28, color: '#b0b0b0', fontWeight: 100 }} className = "text-center">Global Deaths: <span style = {{ color: '#943a3a', fontSize: 35 }}>{totalDeaths.toLocaleString()}</span></p>
                </div>
                <div className = "col-md-3 mx-auto">
                </div>
            </div>
            <div className = "container">  
            <div class="md-form mt-0 input-group" style = {{ padding: 40 }}>
                <div className = "input-group-prepend">
                    <span className = "input-group-text">Search: </span>
                </div>
                <input onChange = {(e) => { alterDisplayData(e.target.value) }} class="form-control" type="text" placeholder="..." aria-label="Search"/>
            </div> 
                <div className = 'container-fluid'>
                    <table className = "table table-hover">
                        <thead style = {{ color: '#474747' }}>
                            <tr>
                                <th scope = "col">#</th> 
                                <th scope = "col">Country</th> 
                                <th scope = "col">Total Cases</th> 
                                <th scope = "col">Total Deaths</th>
                                <th scope = "col">New Cases</th>
                                <th scope = "col">New Deaths</th>
                            </tr>
                        </thead>
                        <tbody>
                            {dataToDisplay.map((country, index) => {

                                try {
                                    return (
                                        <tr key = {index} onClick = {(e) => {passCountryToDetailPage(country.node.id)}}>
                                            <th scope = 'row'>{index + 1}</th> 
                                            <td scope = 'row'>{country.node.name.split('_').join(' ')}</td> 
                                            <td scope = 'row' style = {{ color: '#9e0000' }}>{country.node.totalCases}</td> 
                                            <td scope = 'row'>{country.node.totalDeaths}</td>
                                            <td scope = 'row' style = {{ color: '#615c00' }}>{country.node.history.edges[0].node.newCases}</td>
                                            <td scope = 'row' style = {{ color: '#003b7a' }}>{country.node.history.edges[0].node.newDeaths}</td>
                                        </tr>
                                    )
                                } catch (TypeError) {
                                
                                }
    })}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    )
}  