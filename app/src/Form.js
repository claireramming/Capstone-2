import React, {useState} from 'react'
import {prop_types, room_types, boroughs, neighborhoods} from './lists.js'

const listToOptions = (listArray) => listArray.map((thing, index) => <option key={index} value={`${thing}`}>{thing}</option>)

const propTypes = listToOptions(prop_types)
const roomTypes = listToOptions(room_types)
const boroughNames = listToOptions(boroughs)
const neighborhoodNames = listToOptions(neighborhoods)

function Form({setPred}) {
    const [propType, setPropType] = useState('Apartment')
    const [numRooms, setNumRooms] = useState(0)
    const [numGuests, setNumGuests] = useState(0)
    const [roomType, setRoomType] = useState('Shared room')
    const [borough, setBorough] = useState('Manhattan')
    const [neighborhood, setNeighborhood] = useState('Jackson Heights')

    const entry = {
        prop_type: propType,
        neighborhood: neighborhood,
        borough: borough,
        room_type: roomType,
        num_rooms: numRooms,
        num_accom: numGuests
    }

    async function predictPrice(formData) {
        const response = await fetch('http://localhost:8000/predict', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            mode: 'cors',
            body: JSON.stringify(formData),
        })
        const data = await response.json()
        console.log(data)
        setPred(data.predicted)
    }

    return (
        <form onSubmit={(e)=>{
            e.preventDefault()
            predictPrice(entry)
        }}>
            <label>
                Type of Place:
                <select 
                    value={propType}
                    onChange={(e)=>setPropType(e.target.value)}>
                    {propTypes}
                </select>
            </label>
            <label>
                Number of Bedrooms: 
                <input 
                    type='number'
                    value={numRooms}
                    onChange={(e)=>setNumRooms(e.target.value)}
                /></label>
            <label>
                Number of Guests: 
                <input 
                    type='number'
                    value={numGuests}
                    onChange={(e)=>setNumGuests(e.target.value)}
                    /></label>
            <label>
                Type of Room: 
                <select
                    value={roomType}
                    onChange={(e)=>setRoomType(e.target.value)}>
                    {roomTypes}
                </select>
                </label>
            <label>
                Borough:
                <select
                    value={borough}
                    onChange={(e)=>setBorough(e.target.value)}>
                    {boroughNames}
                </select>
            </label>
            <label>
            Neighborhood: 
            <select
                value={neighborhood}
                onChange={(e)=>setNeighborhood(e.target.value)}>
                {neighborhoodNames}
                </select>
            </label>
            <button>Find Fair Fare</button>
        </form>
    )
}

export default Form