import React, {useState, useEffect} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal} from "semantic-ui-react";
import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";
import axios from 'axios';
import CONFIG from './config';

function GlobalStats(){
    const [data, setData] = useState([{"name": 1, "Counts": 5},
                                      {"name": 2, "Counts": 4},
                                      {"name": 3, "Counts": 3},
                                      {"name": 4, "Counts": 2},
                                      {"name": 5, "Counts": 1}]);

    
    const [busyHours, setBusyHours] = useState([]);
    const [bookedUsers, setBookedUsers] = useState([]);
    const [bookedRooms, setBookedRooms] = useState([]);  
    
    const busyURL = CONFIG.URL + '/global/statistics/buesiesthours'
    const userURL = CONFIG.URL + '/global/statistics/booked/users'
    const roomURL = CONFIG.URL + '/global/statistics/booked/rooms'

    useEffect(() => {
        // fetch top busiest hours
        axios({
            method: 'GET',
            url: busyURL
        })
        .then((res) => {
            let busyHrs = []
            let resData = res.data.busiest_hours
            for(let i = 0; i < resData.length; i++) {
                busyHrs.push({
                    "count": resData[i].count,
                    "interval": resData[i].schedule_start_time + '-' + resData[i].schedule_end_time
                })
            }
            setBusyHours(busyHrs)
        })

        // fetch moost booked users
        axios({
            method: 'GET',
            url: userURL
        })
        .then((res) => setBookedUsers(res.data.most_booked_users))

        // fetch most booked rooms
        axios({
            method: 'GET',
            url: roomURL
        })
        .then((res) => setBookedRooms(res.data.most_booked_rooms))
    }, [])

    return (
    <Container style={{ height: 800 }}>
        <p>Busiest Hours</p>
        <BarChart width={730} height={250} data={busyHours}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="interval"/>
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="count" fill="#8884d8" />
        </BarChart>

        <p>Most Booked Users</p>
        <BarChart width={730} height={250} data={bookedUsers}>
            <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="user_name"
                    angle={10}
                    tickMargin={8} 
                    interval={0}
                    tickSize = {5}
                    style={{
                        fontSize: '0.75rem',
                    }}/>
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="count" fill="#8884d8" />
        </BarChart>

        <p>Most Booked Rooms</p>
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

export default GlobalStats;
