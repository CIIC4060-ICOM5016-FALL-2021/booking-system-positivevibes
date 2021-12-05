import React, {Component, useEffect, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal, Divider, Dropdown} from "semantic-ui-react";
import axios from 'axios';
import Select from 'react-select';

import CONFIG from './config';
import { parseFromDate } from './functions/DateChange';
import 'qs';
import QueryString, { stringify } from 'qs';

function BookMeeting(){
    const [dates, setDates] = useState([]);
    const [roomDates, setRoomDates] = useState([]);
    const [open, setOpen] = useState(false);
    const localizer = momentLocalizer(moment)
    const [rooms, setRooms] = useState([])
    const [selectedRoom, setSelectedRoom] = useState({
                                        'text': 'Select Room',
                                        'value': -1
                                        })
    const [warningText, setWarningText] = useState("");
    const [sucessText, setSucessText] = useState("");
    const room_url = CONFIG.URL + '/rooms';
    const unavail_url = CONFIG.URL + '/room_unavailability';
    const sched_url = CONFIG.URL + '/rooms/schedule';
    const user = JSON.parse(localStorage.getItem('User'));

    useEffect(() => {
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
    }, []);

    const addSelection = (selected) => {
        let date_array = dates;
        console.log(selected);
        date_array.push({
            'title': 'Selection',
            'allDay': false,
            'start': new Date(selected.start),
            'end': new Date(selected.end)
        });
        setDates(date_array);
    }

    const switchRoom = (selected) => {
        setSelectedRoom(selected);
        setTimeout(() => {}, 250);
    }

    const changeSelectedRoom = () => {
        setRoomDates([]);
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

    return (
    <>
    <Container fluid style={{alignItems:"center", justifyContent:"center"}}>
        <Select name="Rooms" class = "ui fluid search dropdown"
            search
            fluid
            options={rooms}
            onChange={switchRoom}
            style={{marginBottom: "1em"}}
        />
        <p/>
        <Button
                    color="blue"
                    onClick={changeSelectedRoom}
                    
        > Select Room </Button>
        <Button
            color="black"
            onClick={markRoom}
        > Mark Room as unavailable </Button>
        <span className="warning">{warningText}</span>
        <span className="success">{sucessText}</span>
        <Divider />
    </Container>
            
    
    <Container style={{ height: 800}}>
        < Calendar
            selectable
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
        
        </Container>
    </>
    )
        


}
export default BookMeeting;
