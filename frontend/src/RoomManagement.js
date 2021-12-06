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
const unavail_url = CONFIG.URL + '/room_unavailability';
const sched_url = CONFIG.URL + '/rooms/schedule';
const user = JSON.parse(localStorage.getItem('User'));

function BookMeeting(){
    const [dates, setDates] = useState([]); // current selected 'event'
    const [roomDates, setRoomDates] = useState([]); // holds parsed r_unavails
    const [open, setOpen] = useState(false);
    const localizer = momentLocalizer(moment);
    const [rooms, setRooms] = useState([]); // get from rooms
    const [selectedRoom, setSelectedRoom] = useState({'text': 'Select Room', 'value': -1});
    const [warningText, setWarningText] = useState("");
    const [sucessText, setSucessText] = useState("");
    const [selected, setSelected] = useState({}); // selected event
    const [rawSchedules, setRawSchedules] = useState([]); // get from r_unavail
    const [allSchedules, setAllSchedules] = useState([]); // get from schedules
    const [showModify, setShowModify] = useState(false); // boolean to show event popup modification
    const [deleteBtn, setDeleteBtn] = useState('hidden'); // delete room visibility
    const [deletePop, setDeletePop] = useState(false); // delete confirmation popup
    const [appointedRoom, setAppointedRoom] = useState({}); // who appointed a room (user)
    const [allInvitees, setAllInvitees] = useState([]); // holds all invitees of selected event
    const [inviteeEmails, setInviteeEmails] = useState(""); // holds all invitee emails of selected event
    const [authLvlText, setAuthLvlText] = useState("<Please Select a Room>"); // to display the auth lvl of room

    const [addRoomOpen, setAddRoomOpen] = useState(false); // boolean to show add room form
    const [modRoomOpen, setModRoomOpen] = useState(false); // boolean to show modify room form

    
    useEffect(() => {
        axios({method: 'GET', url: room_url})
        .then((res) => {
            let room_list = []
            for(let i = 0; i < res.data.length; i++) {
                room_list.push({
                    label: res.data[i].room_name,
                    value: res.data[i].room_id,
                    authorization_level: res.data[i].authorization_level,
                    building_id: res.data[i].building_id,
                    room_capacity: res.data[i].room_capacity
                })
            };
            setRooms(room_list);
        });

        axios({method: 'GET', url: unavail_url})
        .then((res) => {setRawSchedules(res.data)}); 

        axios({method: 'GET', url: CONFIG.URL + '/schedule'})
        .then((res) => setAllSchedules(res.data));
    }, []);

    const switchRoom = (selected) => {
        setSelectedRoom(selected);
        setTimeout(() => {}, 250);
    }

    const changeAuthText = () => {
        // setAuthLvlText(authDictionary[selectedRoom.value.toString()]);
        for(let i = 0; i < rooms.length; i++) {
            if (rooms[i].value == selectedRoom.value) {
                setAuthLvlText(authDictionary[rooms[i].authorization_level.toString()]);
                break;
            }
        }
    }

    const changeSelectedRoom = () => {
        setRoomDates([]);
        setDeleteBtn('visible');
        changeAuthText();
        setTimeout(() => {}, 250);
        let room_dates = []
        let room_selected = {
            room_id : selectedRoom.value,
            user_id : user.user_id,
            date : "none"
        }
        // console.log(room_selected);
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
                tmp[i].room_date.split("-").forEach(s => date_split.push(parseInt(s)));
                tmp[i].room_start_time.split(":").forEach(s => start_split.push(parseInt(s)));
                tmp[i].room_end_time.split(":").forEach(s => end_split.push(parseInt(s)));

                // new Date(year, month, day, hours, minutes, seconds, milliseconds)
                let start_t = new Date(date_split[0], date_split[1]-1, date_split[2], start_split[0], start_split[1], start_split[2], 0);
                let end_t = new Date(date_split[0], date_split[1]-1, date_split[2], end_split[0], end_split[1], end_split[2], 0);
                room_dates.push({
                    'title': tmp[i].slot_name,
                    'allDay': false,
                    'start': start_t,
                    'end': end_t
                });
            }
            setRoomDates(room_dates);
        })
    }

    const markRoom = () => {
        if (selectedRoom.value != -1) {
            if (dates.length >= 1) {
                setWarningText("");
                // console.log(dates);
                let start = dates[0].start.toString();
                let end = dates[0].end.toString();
                console.log(start, end);
                let parsed = parseFromDate(start, end)
                console.log(parsed);
        
                let marking_slot = {
                    "room_id": selectedRoom.value,
                    "room_unavail_date": parsed[0],
                    "room_start_time": parsed[1],
                    "room_end_time": parsed[2]
                }
                
                axios({
                    method: 'POST',
                    url: unavail_url,
                    data: marking_slot,
                    headers: {'Content-Type': 'application/json'}
                })
                .then((res) => {
                    setSucessText("Time marked as unavailable successfully.");
                    setTimeout(function() {
                        //reload page
                        window.location.reload();
                    }, 2000);
                })
            }
            else { // Please select a time frame to mark
                setWarningText("Please select a time frame to mark.");
            }
            
        }
        else { // Please select a room
            setWarningText("Please select a room.");
        }
        
        
    }
    const handleSelectedEvent = (event) => {
        setSelected(event);
        setShowModify(true);
        setAllInvitees([]);
        setInviteeEmails("");
        // console.log(event);
        // console.log(event.start, event.end)

        // fetch who appointed the room
        let e_info = parseFromDate(event.start, event.end);
        //console.log(e_info)
        //console.log(rawSchedules);
        let params = {
            "room_id" : selectedRoom.value,
            "user_id" : user.user_id,
            "date" : e_info[0],
            "time" : e_info[1]
        }

        let sched_id;
        for (let i = 0; i < allSchedules.length; i++) {
            if (allSchedules[i].schedule_date == e_info[0]
                && allSchedules[i].schedule_start_time == e_info[1]
                && allSchedules[i].schedule_end_time == e_info[2]
                && allSchedules[i].room_id == selectedRoom.value) {                    
                sched_id = allSchedules[i].schedule_id;
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
                setAllInvitees(res.data);
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
                user_first_name: "Dept",
                user_last_name: "Staff",
                user_id: -1,
                user_email: "None"
            })
        }

        
    }
        
    const deleteUnavails = (unavail_slots) => {
        // delete all unavailabilities related to the selected room
        // this takes care of schedule, invitees, and both user and room unavailability
        for (let i = 0; i < unavail_slots.length; i++) {
            axios({method: 'DELETE', url: unavail_url + '/' + unavail_slots[i].room_unavail_id});
        }
    }
    const deleteRoomHelper = () => {
        axios({method: 'DELETE', url: room_url + '/' + selectedRoom.value.toString()})
        .then((res) => {
            setDeletePop(false);
            setSucessText('Room deleted! Refreshing page...');
            setTimeout(() => window.location.reload(), 2500);
        })
        .catch((err) => deleteRoomHelper()) // please do not do this elsewhere c:
    }
    const deleteRoom = () => {
        setDeletePop(false);
        setSucessText('Room deleted! Refreshing page...');
        
        let unavail_slots = [];
        axios({method: 'GET', url: unavail_url})
        .then((res) => {
            for (let i = 0; i < res.data.length; i++) {
                let curr = res.data[i];
                if (curr.room_id == selectedRoom.value)
                    unavail_slots.push(curr);
            }            
            deleteUnavails(unavail_slots);
            deleteRoomHelper();            
        });
    }

    const deleteEvent = () => {
        let sched_ID;
        let e_info = parseFromDate(selected.start, selected.end);
        for(let i = 0; i < rawSchedules.length; i++){
            let curr = rawSchedules[i]
            if (curr.room_start_time == e_info[1]
                && curr.room_end_time == e_info[2]
                && curr.room_unavail_date == e_info[0]
                && curr.room_id == selectedRoom.value) {
                //
                sched_ID = curr.room_unavail_id.toString();
                break;
            }
        }
        console.log("Trying to delete event: ", sched_ID.toString());
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
    }

    return (
        <>
            <Container fluid style={{ alignItems: "center", justifyContent: "center" }}>  
                <Popup
                    content='Click the button to add a new room!'
                    position='left center'
                    trigger={
                        <Button
                        color={'green'}
                        content={'Add a Room'}
                        size={'medium'}
                        onClick={() => setAddRoomOpen(true)}
                />}
                />
                <Popup
                    content='Click the modify button to modify the room'
                    position='right center'
                    trigger={
                        <Button
                        color={'orange'}
                        content={'Modify a Room'}
                        size={'medium'}
                        onClick={() => setModRoomOpen(true)}
                    />}
                />
                <Divider/>
            </Container>

            <Container fluid style={{ alignItems: "center", justifyContent: "center" }}>
        <Segment>
        <Label attached='top'>Select a Room from the Dropdown Menu</Label>
        <Select name="Rooms" class = "ui search dropdown"
            search
            options={rooms}
            onChange={switchRoom}
            style={{marginBottom: "1em"}}
        />
                </Segment>
                <Divider />
                <span className="success">Authorization Level: {authLvlText}</span>
                <p/>
                 <Popup
                    content='First select a room from the dropdown
                    and then click the select button to select the room'
                    position='left center'
                    trigger={
                        <Button
                        color={'blue'}
                        onClick={changeSelectedRoom}
                    >
                        Select Room
                    </Button>}
                />
                <Popup
                    content='First select a room from the dropdown
                    and then click the mark button to mark the room as unavailable'
                    position='right center'
                    trigger={
                        <Button
                        color={'black'}
                        onClick={markRoom}
                    >
                        Mark Room as unavailable
                    </Button>}
                />
                <Popup
                    content='After selecting a room, click delete to delete the room'
                    position='right center'
                    trigger={
                         <Button
                        color={'red'}
                        style={{visibility: deleteBtn}}
                        onClick={() => setDeletePop(true)}
                    >
                        Delete Room
                    </Button>}
                />   
        <span className="warning">{warningText}</span>
        <span className="success">{sucessText}</span>
        <Divider />
    </Container>
            
    
    <Container style={{ height: 800}}>
        < Calendar
            selectable
            selected={selected}
            onSelectEvent={handleSelectedEvent}
            localizer={localizer}
            startAccessor="start"
            events={roomDates.concat(dates)}
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
                    <Button onClick={deleteEvent} color="red">Delete Event</Button>
                    <Button onClick={() => setShowModify(false)} color="green">CLOSE</Button>
            </Modal.Actions>
        </Modal>

        <Modal
            centered={false}
            size={'tiny'}
            style={{
                height: "fit-content",
                width: "fit-content",
                marginLeft: "25%",
                marginTop:"10%",
            }}
            open={deletePop}
            dimmer={'blurring'}
            onClose={() => setDeletePop(false)}
            onOpen={() => setDeletePop(true)}
        >
            <Modal.Header>Are you sure you want to delete {selectedRoom.label}?</Modal.Header>
            <Modal.Content>This will delete everything related to this room including schedules.</Modal.Content>
                <Modal.Actions>
                    <Button onClick={deleteRoom} color="red">Delete Room</Button>
                    <Button onClick={() => setDeletePop(false)}>Cancel</Button>
            </Modal.Actions>
        </Modal>

        
        <Modal
            centered={true}
            open={addRoomOpen}
            onClose={() => setAddRoomOpen(false)}
            onOpen={() => setAddRoomOpen(true)}         
            >
            <Modal.Content>
                <AddRoom/>
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setAddRoomOpen(false)}>CLOSE</Button>
            </Modal.Actions>
        </Modal>

        <Modal
            centered={true}
            open={modRoomOpen}
            onClose={() => setModRoomOpen(false)}
            onOpen={() => setModRoomOpen(true)}         
            >
            <Modal.Content>
                <ModifyRoom/>
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setModRoomOpen(false)}>CLOSE</Button>
            </Modal.Actions>
        </Modal>
        
    </Container>
    </>
    )
        


}
export default BookMeeting;
