import React from 'react' 
import { gql } from 'apollo-boost' 
import { useQuery } from '@apollo/react-hooks'  

const GET_DATABASE_UDPATE = gql`
{
    allUpdates(first: 1) {
        edges {
            node {
                date
            }
        }
    }
}
`

export default function DatabaseDetail() {
    
    const { loading, error, data } = useQuery(GET_DATABASE_UDPATE) 

    if (loading) return <p>last update...</p> 

    return (
        <p className = "text-right" style = {{ color: '#ababab' }}>
            last update: {data.allUpdates.edges[0].node.date}
        </p>
    )
}