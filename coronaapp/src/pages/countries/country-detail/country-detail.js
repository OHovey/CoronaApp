import React from 'react' 
import { gql } from 'apollo-boost'
import { useQuery } from '@apollo/react-hooks'
import { useHistory, useParams } from 'react-router-dom'

import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, ReferenceLine, ReferenceArea,
    ReferenceDot, Tooltip, CartesianGrid, Legend, Brush, ErrorBar, AreaChart, Area,
    Label, LabelList, BarChart, Bar } from 'recharts';

const GET_COUNTRY = gql`
    query country($id: ID!) {
        country(id: $id) {
            id
            name
            totalCases
            totalDeaths
            history {
                edges {
                    node {
                        date 
                        newCases 
                        newDeaths
                    }
                }
            }
        }
    }
`;


function returnUniqueArray(array) {
    const result = [] 
    const map = new Map() 
    for (const item of array) {
        if (!map.has(item.date)) {
            map.set(item.date, true)
            result.push({
                date: item.date,
                'New Cases': item['New Cases'],
                'New Deaths': item['New Deaths']
            })
        }
    }
    return result
}


export default function CountryDetail() {
    let history = useHistory()

    const { countryId } = useParams()

    const { loading, error, data } = useQuery(GET_COUNTRY, {
        variables: { id: countryId }
    }) 

    if (loading) return <p>Loading...</p>

    let AdditionYSpace = 0
    if (data.country.totalCases < 500) {
        AdditionYSpace = 50
    }
    else if (data.country.totalCases < 1000) {
        AdditionYSpace = 250
    } else if (data.country.totalCases > 1000) {
        AdditionYSpace = 500
    } else if (data.country.totalCases > 10000) {
        AdditionYSpace = 3000
    }
    
    
    let case_data = data.country.history.edges
    console.log(case_data)
    try {
        if (data.country.history.edges[0].node.newCases > data.country.history.edges[data.country.history.edges.length - 1].node.newCases) {
            case_data = case_data.reverse()
        } 
    } catch (TypeError) {

    }
    
    // ------------------------------------------------------------------------
    // sort data iinto new, more accessible arrays sorted by total accumulated 
    // death and case data
    const arrSumCases = arr => arr.reduce((a,b) => a + b.node.newCases, 0)
    const arrSumDeaths = arr => arr.reduce((total, d) => total + d.node.newDeaths, 0)
    let accumulated_case_data = Array.from(case_data, (case_object, i) => {    
        // console.log('case_data: ' + case_object)
        let dayDataPoint = {} 
        dayDataPoint['date'] = case_object.node.date
        dayDataPoint['Total Cases'] = arrSumCases(case_data.slice(0, i))
        dayDataPoint['Total Deaths'] = arrSumDeaths(case_data.slice(0, i))
        return dayDataPoint
    })
    // accumulated_case_data = returnUniqueArray(accumulated_case_data) 

    let accumulated_death_data = Array.from(case_data, (case_object, i) => {
        let dayDataPoint = {} 
        dayDataPoint['date'] = case_object.node.date 
        dayDataPoint['New Cases'] = case_object.node.newCases 
        dayDataPoint['New Deaths'] = case_object.node.newDeaths 
        return dayDataPoint
    })
    if (new Set(accumulated_case_data.map(item => item.date)).length > accumulated_case_data.length) {
        accumulated_case_data = accumulated_case_data.slice(0, (accumulated_case_data.length / 2))
        accumulated_death_data = accumulated_death_data.slice(0, (accumulated_death_data.length / 2))
    }
    // accumulated_death_data = returnUniqueArray(accumulated_death_data)
    // console.log('accumulated death data: ' + JSON.stringify(accumulated_death_data))

    accumulated_case_data = accumulated_case_data.sort((a, b) => Date(b.date) - Date(a.date))
    console.log('accumulated case data: ' + JSON.stringify(accumulated_case_data))
    // -------------------------------------
    // split data by the first case measured
    let sliceIndex = 0
    for (let i = 0; i < accumulated_case_data.length; i++) {
        console.log('accumulated: ' + accumulated_case_data[i])
        if (accumulated_case_data[i]['Total Cases'] > 0) {
            sliceIndex = i 
            break 
        }
    }
    console.log('sliceIndex: ' + sliceIndex)
    accumulated_case_data = accumulated_case_data.slice(sliceIndex - 1, accumulated_case_data.length - 1) 
    accumulated_death_data = accumulated_death_data.slice(sliceIndex - 1, accumulated_death_data.length - 1)



    return (
        <div className = 'container-fluid'
            style = {{
                fontWeight: 0.5,
                padding: 0
            }}
        >
            <h3 style = {{ color: 'whitesmoke', margin: 0, paddingLeft: 32 }} className = "bg-dark" onClick = {(e) => { history.goBack() }}><span style = {{ backgroundColor: 'whitemoke', borderRadius: 10 }}>{"\u2190"}</span> back</h3>
            
            <hr style = {{ margin: 0, backgroundColor: '#636363' }}></hr>
            <div className = 'container-fluid align-items-center bg-dark' style = {{ padding: 0 }}>
                <div className = "row bg-dark">
                    <div className = "col-md-12 align-items-center">
                        <h1 className = "mx-auto" style = {{ paddingLeft: 30, fontSize: '3.5em', color: 'whitesmoke' }} >{data.country.name.split('_').join(' ')}</h1>
                    </div>
                </div>
                <hr style = {{ backgroundColor: "#636363", margin: 0 }}/>
                <div className = "container-fluid" style = {{ backgroundColor: '#636363' }}>
                    <div className = "row">
                        <div className = "col-md-6" style = {{ paddingLeft: '12%' }}>
                            <h2
                                style = {{ color: '#eb4034' }}
                            >Total Cases: <span style = {{ fontSize: '1.3em', color: '#ff5454', display: 'inline-block' }}>{data.country.totalCases}</span></h2>
                        </div>
                        <div className = "col-md-6" style = {{ paddingLeft: '12%' }}>
                            <h2 style = {{ color: 'whitesmoke'  }}>Total Deaths: <h1 style = {{ fontSize: '1.3em', display: 'inline-block' }}>{data.country.totalDeaths}</h1></h2>
                        </div>
                    </div>
                </div>
                <hr style = {{ backgroundColor: "#636363", margin: 0 }}/>
            </div>
            <div className = "container">
                <h3 style = {{ margin: 40, borderBottomStyle: 'solid', borderBottomColor: 'black' }}>Total Cases and Deaths over time - from earliest case</h3>
                <br/>
                <ResponsiveContainer width = "100%" height = {400}>
                    <LineChart data={accumulated_case_data}>
                        <CartesianGrid strokeDasharray="3 3" fill = "white" />
                        <XAxis type="category" dataKey="date" height={40}>
                            <Label value="Date" position="insideBottom" />
                        </XAxis>
                        <YAxis type = "number" dataKey="New Cases" width = {80} domain = {[0, Math.ceil( (data.country.totalCases + AdditionYSpace) / 100) * 100]}>
                            <Label value = "no of cases" position = "insideLeft" angle = {90} />
                        </YAxis>
                        <Legend verticalAlign = "top" height = {40} value = "New Cases" />
                        <Tooltip />
                        <Label value = "Total COVID-19 infection cases and deaths over time" position='insideTopLeft' />
                        <Line
                            type="monotone"
                            dataKey="Total Cases"
                            stroke="#ff5252"
                            >
                                {/* <LabelList dataKey = "Total Cases" /> */}
                        </Line>
                        <Line 
                            type = "monotone"
                            dataKey = "Total Deaths" 
                            stroke = "#000000"
                            fill = "#731d1d"
                        />
                        {/* <LabelList dataKey = "Total Deaths" /> */}
                    </LineChart>
                </ResponsiveContainer>
                <br/>
                <hr/>
                <br/>
                <h3 style = {{ margin: 40, borderBottomStyle: 'solid', borderBottomColor: 'black' }}>Day to Day Statistics - from earliest case</h3>
                <ResponsiveContainer width = "100%" height = {400}>
                    <BarChart width={730} height={250} data={accumulated_death_data}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip label = "date" />
                        <Legend />
                        <Bar dataKey="New Cases" fill="#ff5252" barSize = {[{'width': 40}]} />
                        <Bar dataKey="New Deaths" fill="#000000" />
                    </BarChart>
                </ResponsiveContainer>
            </div>
            
            {/* <div className='line-chart-wrapper'> */}
        {/* </div> */}
        </div>
    )
}