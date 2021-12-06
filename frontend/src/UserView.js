import React, {Component, useEffect, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal, Tab} from "semantic-ui-react";
import BookMeeting from "./BookMeeting";
import Schedule from "./Schedule";
import LogOut from "./LogOut";
import UserStats from './UserStats';
import RoomManagement from './RoomManagement';
import Profile from './Profile';
//import './UserView.css';

function UserView(){
    const [isAuth, setIsAuth] = useState(false)
    const user = JSON.parse(localStorage.getItem('User'))
    if (!user)
        window.location.href = window.location.origin + "/Home"

    useEffect(() => {
        if (user['authorization_level'] == 2) // 2 is the highest auth_lvl
            setIsAuth(true)
    }, [])

    console.log("Authorized", isAuth)
        
    const panes = [
        {
            menuItem: 'Booking', render: () => <BookMeeting/>
        },
        {
            menuItem: 'Schedule', render: () => <Schedule/>
        }
    ]

    if(isAuth)
        panes.push({
            menuItem: 'Room Management', render: () => <Tab.Pane active={isAuth} renderActiveOnly={true}><RoomManagement/></Tab.Pane>
        })
    
    panes.push({
        menuItem: 'User Statistics', render: () => <UserStats/>
    })
    panes.push({
        menuItem: 'Dashboard', render: () => {window.location.href = window.location.origin + '/Dashboard'}
    })
     panes.push({
        menuItem: 'Profile', render: () => <Profile/>
    })
    panes.push({
        menuItem: 'Log out', render: () => <LogOut/>
    })

    return <Tab panes={panes} menu={{color:"black", inverted: true}}/>

}
export default UserView;
