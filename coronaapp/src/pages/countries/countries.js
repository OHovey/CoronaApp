import React from 'react' 
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

function sortCountriesByInfectedCount(a, b) {
    if (a.node.totalCases < b.node.totalCases) return 1 
    if (b.node.totalCases < a.node.totalCases) return -1 

    return 0;
}

export default function Countries() {
    
    const { loading, error, data } = useQuery(GET_COUNTRIES)

    let history = useHistory()

    // console.log('data: ' + data)

    if (loading) return <p>Loading...</p>

    data.allCountries.edges.map(country => {
        try {
            console.log(country.node.history.edges[0]['node'])
        } catch (TypeError) {
            
        }
    })

    data.allCountries.edges.sort(sortCountriesByInfectedCount)

    function sumCases(arr, key) {
        return arr.reduce((a, b) => a + (b.node[key] || 0), 0);
    }
    
    let totalCases = sumCases(data.allCountries.edges, 'totalCases')
    let totalDeaths = sumCases(data.allCountries.edges, 'totalDeaths')

    function passCountryToDetailPage(countryId) {
        history.push('/country/' + countryId)
    }

    return (
        <div className = 'container-fluid' style = {{ backgroundColor: '#bfbfbf' }}>
            <div className = "row bg-dark">
                <div className = "col-md-3 mx-auto">
                </div>
                <div className = "col-md-3 align-middle">
                    <p style = {{ fontSize: 28, color: 'whitesmoke' }} className = "text-center">Global Cases: <span style = {{ color: '#FF4136', fontSize: 35 }}>{totalCases}</span></p>
                </div>
                <div className = "col-md-3 mg-auto">
                    <p style = {{ fontSize: 28, color: 'whitesmoke' }} className = "text-center">Global Deaths: <span style = {{ color: '#8c4f4f', fontSize: 35 }}>{totalDeaths}</span></p>
                </div>
                <div className = "col-md-3 mx-auto">
                </div>
            </div>
            <div className = "container">    
                <div className = 'container-fluid'>
                    <table className = "table table-hover">
                        <thead>
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
                            {data.allCountries.edges.map((country, index) => {

                                try {
                                    return (
                                        <tr key = {index} onClick = {(e) => {passCountryToDetailPage(country.node.id)}}>
                                            <th scope = 'row'>{index + 1}</th> 
                                            <td scope = 'row'>{country.node.name}</td> 
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