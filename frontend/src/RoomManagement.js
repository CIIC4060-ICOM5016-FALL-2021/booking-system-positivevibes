import React, {Component, useEffect, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal, Divider, Dropdown} from "semantic-ui-react";
import axios from 'axios';
import Select from 'react-select';

import CONFIG from './config';
import { parseFromDate } from './functions/DateChange';

function BookMeeting(){
    const [dates, setDates] = useState([]);
    const [open, setOpen] = useState(false);
    const localizer = momentLocalizer(moment)
    const [rooms, setRooms] = useState([])
    const [selectedRoom, setSelectedRoom] = useState({
                                        'text': 'Select Room',
                                        'value': -1
                                        })
    const [warningText, setWarningText] = useState("");
    const [sucessText, setSucessText] = useState("");
    const url = CONFIG.URL + '/rooms'

    useEffect(() => {
        axios({
            method: 'GET',
            url: url
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
                
                let unavail_url = CONFIG.URL + '/room_unavailability';

                axios({
                    method: 'POST',
                    url: unavail_url,
                    data: marking_slot,
                    headers: {'Content-Type': 'application/json'}
                })
                .then((res) => {
                    setSucessText("Time marked as unavailable successfully.");
                    Promise(resolve => setTimeout(resolve, 2000));
                    //reload page
                    window.location.reload();
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
            onChange={(selected) => setSelectedRoom(selected)}
            style={{marginBottom: "1em"}}
        />
        <p/>
        {/* <Button
                    color="blue"
                    onClick={() => { setOpen(true) }}
                    
        > Book Meeting </Button> */}
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
            events={dates}
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
