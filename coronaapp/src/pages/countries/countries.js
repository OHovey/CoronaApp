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
        // console.log(country.node)
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
        <div className = 'container-fluid'>
            <div className = "row bg-dark">
                <div className = "col-md-3 mx-auto">
                </div>
                <div className = "col-md-3 mx-auto">
                    <p style = {{ fontSize: 28, color: 'whitesmoke' }} className = "mx-auto">allCases: <span style = {{ color: '#FF4136' }}>{totalCases}</span></p>
                </div>
                <div className = "col-md-3 mx-auto">
                    <p style = {{ fontSize: 28, color: 'whitesmoke' }} className = "mx-auto">All deaths: <span>{totalDeaths}</span></p>
                </div>
                <div className = "col-md-3 mx-auto">
                </div>
            </div>
            <div className = 'container'>
                <table className = "table table-hover">
                    <thead>
                        <tr>
                            <th scope = "col">#</th> 
                            <th scope = "col">Country</th> 
                            <th scope = "col">Total Cases</th> 
                            <th scope = "col">Total Deaths</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.allCountries.edges.map((country, index) => (
                            <tr key = {index} onClick = {(e) => {passCountryToDetailPage(country.node.id)}}>
                                <th scope = 'row'>{index + 1}</th> 
                                <td scope = 'row'>{country.node.name}</td> 
                                <td scope = 'row'>{country.node.totalCases}</td> 
                                <td scope = 'row'>{country.node.totalDeaths}</td>
                                {/* <td scope = 'row'>{country.node.history.}</td> */}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    )
}  