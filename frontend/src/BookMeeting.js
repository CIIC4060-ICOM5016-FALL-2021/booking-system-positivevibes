import React, {useEffect, useState} from 'react';
import {Calendar, momentLocalizer} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Container, Modal} from "semantic-ui-react";
import axios from 'axios';

import CONFIG from './config';
import { parseFromDate } from './functions/DateChange';

const authDictionary = {
    "0": "Student",
    "1": "Professor",
    "2": "Department Staff"
}

const room_url = CONFIG.URL + '/rooms';
const unavail_url = CONFIG.URL + '/user_unavailability';
const sched_url = CONFIG.URL + '/users/schedule';
const user = JSON.parse(localStorage.getItem('User'));

function BookMeeting(){
    const [open, setOpen] = useState(false);
    const [dates, setDates] = useState([]); // current selected 'event'
    const [userDates, setUserDates] = useState([]); // holds parsed r_unavails
    const localizer = momentLocalizer(moment);
    const [selected, setSelected] = useState({}); // selected event
    const [allSchedules, setAllSchedules] = useState([]); // get from schedules
    const [showModify, setShowModify] = useState(false); // boolean to show event popup modification
    const [appointedRoom, setAppointedRoom] = useState({}); // who appointed a room (user)
    const [allInvitees, setAllInvitees] = useState([]); // holds all invitees of selected event
    const [inviteeEmails, setInviteeEmails] = useState(""); // holds all invitee emails of selected event
    const [rawSchedules, setRawSchedules] = useState([]); // get from r_unavail
    const [selectedRoom, setSelectedRoom] = useState({'text': 'Select Room', 'value': -1});
    const [sucessText, setSucessText] = useState("");
    const [selectedEventID, setSelectedEventID] = useState();
    const [warningText, setWarningText] = useState("");

    useEffect(() => {
        setUserDates([]);

        setTimeout(() => {}, 250);
        let user_dates = []
        let room_selected = {
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
        axios({method: 'GET', url: unavail_url})
        .then((res) => {setRawSchedules(res.data)}); 
        axios({method: 'GET', url: CONFIG.URL + '/invitee'})
        .then((res) => setAllInvitees(res.data));
    }, []);


    const handleSelectedEvent = (event) => {
        setWarningText("")
        setSelected(event);
        setShowModify(true);
        //setAllInvitees([]);
        setInviteeEmails("");

        // fetch who appointed the room
        let e_info = parseFromDate(event.start, event.end);
        let params = {
            "date" : e_info[0],
            "time" : e_info[1],
            "room_id" : -1
        }

        let sched_id;
        for (let i = 0; i < allSchedules.length; i++) {
            if (allSchedules[i].schedule_date == e_info[0]
                && allSchedules[i].schedule_start_time == e_info[1]
                && allSchedules[i].schedule_end_time == e_info[2]) {    
                    let found = false; 

                    for(let j = 0; j < allInvitees.length; j++){

                        if(allInvitees[j].schedule_id == allSchedules[i].schedule_id &&
                            allInvitees[j].user_id == user.user_id){

                                sched_id = allSchedules[i].schedule_id;
                                params.room_id = allSchedules[i].room_id
                                found = true;
                                setSelectedEventID(sched_id);
                                console.log(sched_id)
                                break;

                            }
                    }         
                    if(found)
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

    const deleteEvent = () => {
        let sched_ID;
        let e_info = parseFromDate(selected.start, selected.end);
        console.log(rawSchedules)
        for(let i = 0; i < rawSchedules.length; i++){
            let curr = rawSchedules[i]
            if (curr.user_start_time == e_info[1]
                && curr.user_end_time == e_info[2]
                && curr.user_date == e_info[0]
                && curr.user_id == user.user_id) {
                    if(curr.scheduled == 0){
                        sched_ID = curr.user_unavail_id.toString();
                        break;
                    }
                    else{
                        console.log(selectedEventID)
                        for(let j = 0; j < allSchedules.length; j++){
                            if(allSchedules[j].schedule_id == selectedEventID){
                                if(allSchedules[j].user_id == user.user_id){
                                    sched_ID = curr.user_unavail_id.toString();
                                    break;
                                }
                                break;
                            }
                        }
                    }
                
            }
        }
        console.log("Trying to delete event: ", sched_ID);
        axios({
            method: 'DELETE',
            url: unavail_url +"/"+ sched_ID
        })
        .then((res) => {
            console.log("Success!")
            setShowModify(false);
            setSucessText('Event deleted! Refreshing page...')
            setTimeout(function() {
                //reload page
                window.location.reload();
            }, 2500);
        })
        .catch((err) => console.log(err))
        setWarningText("Your are not host of event.")
    }

        return <Container style={{ height: 800 }}>
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
                    <Button onClick={deleteEvent} color="orange">Modify Event</Button>
                    <Button onClick={deleteEvent} color="red">Delete Event</Button>
                    <span className="warning">{warningText}</span>
                    <Button onClick={() => setShowModify(false)} color="green">CLOSE</Button>
            </Modal.Actions>
        </Modal>
        <Modal
            centered={false}
            open={open}
            onClose={() => setOpen(false)}
            onOpen={() => setOpen(true)}
        >
            <Modal.Header>Needs changing!</Modal.Header>
            <Modal.Content>
                <Modal.Description>
                    This is a modal but it serves to show how buttons and functions can be implemented.
                </Modal.Description>
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setOpen(false)}>OK</Button>
            </Modal.Actions>
        </Modal>
        <Container fluid>
        <Button
            fluid
            onClick={() => {setOpen(true)}}
        > Book Meeting </Button>
        <Button
            fluid
            onClick={() => {setOpen(true)}}
        > Mark time as unavailable</Button>
    </Container>
    </Container>


}
export default BookMeeting;
