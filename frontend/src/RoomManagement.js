import React, {Component, useEffect, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal, Divider, Dropdown} from "semantic-ui-react";
import axios from 'axios';
import Select from 'react-select';

import CONFIG from './config';
import { parseFromDate } from './functions/DateChange';
import AddRoom from './functions/AddRoom';

function BookMeeting(){
    const [dates, setDates] = useState([]);
    const [roomDates, setRoomDates] = useState([]);
    const [open, setOpen] = useState(false);
    const localizer = momentLocalizer(moment);
    const [rooms, setRooms] = useState([]);
    const [selectedRoom, setSelectedRoom] = useState({'text': 'Select Room', 'value': -1});
    const [warningText, setWarningText] = useState("");
    const [sucessText, setSucessText] = useState("");
    const [selected, setSelected] = useState({});
    const [rawSchedules, setRawSchedules] = useState([]);
    const [showModify, setShowModify] = useState(false);
    const [deleteBtn, setDeleteBtn] = useState('hidden');
    const [deletePop, setDeletePop] = useState(false);
    const [appointedRoom, setAppointedRoom] = useState({});

    const room_url = CONFIG.URL + '/rooms';
    const unavail_url = CONFIG.URL + '/room_unavailability';
    const sched_url = CONFIG.URL + '/rooms/schedule';
    const user = JSON.parse(localStorage.getItem('User'));

    const loadRooms = () => {
        axios({
            method: 'GET',
            url: room_url
        })
        .then((res) => {
            let room_list = []
            for(let i = 0; i < res.data.length; i++) {
                room_list.push({
                    label: res.data[i].room_name,
                    value: res.data[i].room_id
                })
            };
            setRooms(room_list);
            // console.log(res.data);
        });
    }
    
    loadRooms();    

    const toggleAddRoom = () => {
        setOpen(!open);
    }

    const switchRoom = (selected) => {
        setSelectedRoom(selected);
        setTimeout(() => {}, 250);
    }

    const changeSelectedRoom = () => {
        setRoomDates([]);
        setDeleteBtn('visible');
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
            setRawSchedules(tmp);
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
                console.log(dates);
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
        // console.log(event);
        // console.log(event.start, event.end)

        // fetch who appointed the room
        let e_info = parseFromDate(event.start, event.end);
        // console.log(e_info)
        let params = {
            "room_id" : selectedRoom.value,
            "user_id" : user.user_id,
            "date" : e_info[0],
            "time" : e_info[1]
        }
        axios({
            method: 'GET',
            params: params,
            url: CONFIG.URL + '/rooms/appointed'
        })
        .then((res) => setAppointedRoom(res.data))
    }
        
    const deleteRoom = () => {
        setDeletePop(false);
        setSucessText('Room deleted! Refreshing page...')
        console.log("Trying to delete room with id: ", selectedRoom.value.toString());
        setTimeout(function() {
            //reload page
            window.location.reload();
        }, 5000);
        // axios({
        //     method: 'DELETE',
        //     url: CONFIG.URL + '/rooms/' + selectedRoom.value.toString()
        // })
        // .then((res) => {
        //     setDeletePop(false);
        //     setSucessText('Room deleted! Refreshing page...')
        //     console.log("Trying to delete room with id: ", selectedRoom.value.toString());
        //     setTimeout(function() {
        //         //reload page
        //         window.location.reload();
        //     }, 5000);
        // })
        // .catch((err) => {

        // })
    }

    return (
    <>

    <Modal
        centered={true}
        open={open}
        onClose={() => setOpen(false)}
        onOpen={() => setOpen(true)}>
        <Modal.Content>
            <AddRoom/>
        </Modal.Content>
        <Modal.Actions>
            <Button onClick={() => setOpen(false)}>CLOSE</Button>
        </Modal.Actions>
    </Modal>

    <Container fluid style={{alignItems:"center", justifyContent:"center"}}>
        <Button color="green" content='Add Room' size='big' onClick={toggleAddRoom}/>
        <Divider />
    </Container>

    <Container fluid style={{alignItems:"center", justifyContent:"center"}}>
        <Select name="Rooms" class = "ui fluid search dropdown"
            search
            fluid
            options={rooms}
            onChange={switchRoom}
            style={{marginBottom: "1em"}}
        />
         <Divider />
        <Button
            color="blue"
            onClick={changeSelectedRoom}
        > Select Room </Button>
        <Button
            color="black"
            onClick={markRoom}
        > Mark Room as unavailable </Button>
        <Button
            color="red"
            style={{visibility: deleteBtn}}
            onClick={() => setDeletePop(true)}
        > Delete Room </Button>
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
            trigger={<Button>Show Modal</Button>}
        >
            <Modal.Header>{user.user_name}</Modal.Header>
                <Modal.Content>Scheduled by: {appointedRoom}</Modal.Content>
                <Modal.Actions>
                    <Button color="orange">Modify Event</Button>
                    <Button color="red">Delete Event</Button>
                <Button onClick={() => setShowModify(false)} color="green">Close Modal</Button>
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
            trigger={<Button>Show Modal</Button>}
        >
            <Modal.Header>Are you sure you want to delete {selectedRoom.label}?</Modal.Header>
            <Modal.Content>This will delete everything related to this room including schedules.</Modal.Content>
                <Modal.Actions>
                    <Button onClick={deleteRoom} color="red">Delete Room</Button>
                    <Button onClick={() => setDeletePop(false)}>Cancel</Button>
            </Modal.Actions>
        </Modal>
        
    </Container>
    </>
    )
        


}
export default BookMeeting;
