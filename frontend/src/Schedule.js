import React, {Component, useEffect, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal, Divider, Dropdown, Segment, Popup, Label} from "semantic-ui-react";
import axios from 'axios';
import Select from 'react-select';

import CONFIG from './config';
import { parseFromDate } from './functions/DateChange';
import AddRoom from './functions/AddRoom';
import ModifyRoom from './functions/ModifyRoom';
//import './RoomManagement.css';

const authDictionary = {
    "0": "Student",
    "1": "Professor",
    "2": "Department Staff"
}
const room_url = CONFIG.URL + '/rooms';
const unavail_url = CONFIG.URL + '/user_unavailability';
const sched_url = CONFIG.URL + '/users/schedule';
const user = JSON.parse(localStorage.getItem('User'));

// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }


function Schedule(){

    const [dates, setDates] = useState([]); // current selected 'event'
    const [userDates, setUserDates] = useState([]); // holds parsed r_unavails
    const localizer = momentLocalizer(moment);
    const [selected, setSelected] = useState({}); // selected event
    const [allSchedules, setAllSchedules] = useState([]); // get from schedules
    const [showModify, setShowModify] = useState(false); // boolean to show event popup modification
    const [appointedRoom, setAppointedRoom] = useState({}); // who appointed a room (user)
    //const [allInvitees, setAllInvitees] = useState([]); // holds all invitees of selected event
    const [inviteeEmails, setInviteeEmails] = useState(""); // holds all invitee emails of selected event

    useEffect(() => {
        setUserDates([]);

        setTimeout(() => {}, 250);
        let user_dates = []
        let room_selected = {
            //room_id : selectedRoom.value,
            user_id : user.user_id,
            date : "none"
        }
        axios({
            method: 'GET',
            params: room_selected,
            url: sched_url
        })
        .then((res) => {
            let tmp = []
            for (let i = 0; i < res.data['Non-Scheduled'].length; i++)
                tmp.push(res.data['Non-Scheduled'][i]);
            for (let i = 0; i < res.data['Scheduled'].length; i++)
                tmp.push(res.data['Scheduled'][i]);

                /*{
                'title': 'Selection',
                'allDay': false,
                'start': new Date(selected.start),
                'end': new Date(selected.end)
            } */
            for (let i = 0; i < tmp.length; i++) {
                let date_split = []
                let start_split = []
                let end_split = []
                tmp[i].user_date.split("-").forEach(s => date_split.push(parseInt(s)));
                tmp[i].user_start_time.split(":").forEach(s => start_split.push(parseInt(s)));
                tmp[i].user_end_time.split(":").forEach(s => end_split.push(parseInt(s)));

                // new Date(year, month, day, hours, minutes, seconds, milliseconds)
                let start_t = new Date(date_split[0], date_split[1]-1, date_split[2], start_split[0], start_split[1], start_split[2], 0);
                let end_t = new Date(date_split[0], date_split[1]-1, date_split[2], end_split[0], end_split[1], end_split[2], 0);
                user_dates.push({
                    'title': tmp[i].slot_name,
                    'allDay': false,
                    'start': start_t,
                    'end': end_t
                });
            }
            setUserDates(user_dates);
        })
        axios({method: 'GET', url: CONFIG.URL + '/schedule'})
        .then((res) => setAllSchedules(res.data));
    }, []);


    const handleSelectedEvent = (event) => {
        setSelected(event);
        setShowModify(true);
        //setAllInvitees([]);
        setInviteeEmails("");

        // fetch who appointed the room
        let e_info = parseFromDate(event.start, event.end);
        let params = {
            "user_id" : user.user_id,
            "date" : e_info[0],
            "time" : e_info[1]
        }
        
        let sched_id;
        for (let i = 0; i < allSchedules.length; i++) {
            if (allSchedules[i].schedule_date == e_info[0]
                && allSchedules[i].schedule_start_time == e_info[1]
                && allSchedules[i].schedule_end_time == e_info[2]) {                    
                sched_id = allSchedules[i].schedule_id;
                params.room_id = allSchedules[i].room_id
                break;
            }
        }

        if (sched_id){
            axios({
                method: 'GET',
                params: params,
                url: CONFIG.URL + '/rooms/appointed'
            })
            .then((res) => setAppointedRoom(res.data))
            axios({method: 'GET', url: CONFIG.URL + '/invitee/schedule/' + sched_id.toString()})
            .then((res) => {
                let emailString = ""
                for (let i = 0; i < res.data.length; i++) {
                    if (i != res.data.length - 1) 
                        emailString += res.data[i].user_email + ", "
                    else
                        emailString += res.data[i].user_email
                }
                setInviteeEmails(emailString);
            })
        }
        else{
            setAppointedRoom({
                user_first_name: user.first_name,
                user_last_name: user.last_name,
                user_id: user.user_id,
                user_email: user.user_email
            })
        }
        
    }
        

    return (
    
    
    <Container style={{ height: 800}}>
        < Calendar
            selectable
            selected={selected}
            onSelectEvent={handleSelectedEvent}
            localizer={localizer}
            startAccessor="start"
            events={userDates.concat(dates)}
            endAccessor="end"
            views={["month", "day"]}
            defaultDate={Date.now()}
            onSelecting = {(selected) => setDates([{
                'title': 'Selection',
                'allDay': false,
                'start': new Date(selected.start),
                'end': new Date(selected.end)
            }])}
                        >            
        </Calendar>

        <Modal
            centered={false}
            size={'tiny'}
            style={{
                height: "fit-content",
                width: "fit-content",
                marginLeft: "25%",
                marginTop:"10%",
            }}
            open={showModify}
            dimmer={'blurring'}
            onClose={() => setShowModify(false)}
            onOpen={() => setShowModify(true)}
        >
            <Modal.Header>{user.user_name}</Modal.Header>
                <Modal.Content>Scheduled by: {appointedRoom.user_first_name+' '+appointedRoom.user_last_name}</Modal.Content>
                <Modal.Content>{inviteeEmails == "" ? "" : `Invited users: ${inviteeEmails}`}</Modal.Content>
                <Modal.Actions>
                    <Button onClick={() => setShowModify(false)} color="green">CLOSE</Button>
            </Modal.Actions>
        </Modal>

    </Container>
    )


}
export default Schedule;
