import React, {useState, useEffect} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal} from "semantic-ui-react";
import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";
import axios from 'axios';
import CONFIG from './config';

function UserStats(){
    const [data, setData] = useState([{"name": 1, "Counts": 5},
                                      {"name": 2, "Counts": 4},
                                      {"name": 3, "Counts": 3},
                                      {"name": 4, "Counts": 2},
                                      {"name": 5, "Counts": 1}]);

    const [bookedUsers, setBookedUsers] = useState([]);
    const [bookedRooms, setBookedRooms] = useState([]);  
    
    const user = JSON.parse(localStorage.getItem('User'));
    const userID = user.user_id.toString()
    const userURL = CONFIG.URL + '/users/statistics/' + userID + '/user';
    const roomURL = CONFIG.URL + '/users/statistics/' + userID + '/room';

    console.log(roomURL);
    console.log(userURL);

    useEffect(() => {
        // fetch most booked with user
        axios({
            method: 'GET',
            url: userURL
        })
        .then((res) => setBookedUsers([res.data]))

        // fetch most used room
        axios({
            method: 'GET',
            url: roomURL
        })
        .then((res) => setBookedRooms([res.data]))
    }, [])

    return (
        // <p>Hellowa</p>
    <Container style={{ height: 800 }}>

        <p>Most Booked With User</p>
        <BarChart width={730} height={250} data={bookedUsers}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="most_booked_user_name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="count" fill="#8884d8" />
        </BarChart>

        <p>Most Used Room</p>
        <BarChart width={730} height={250} data={bookedRooms}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="room_name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="count" fill="#8884d8" />
        </BarChart>
    </Container>
    )
}

export default UserStats;
