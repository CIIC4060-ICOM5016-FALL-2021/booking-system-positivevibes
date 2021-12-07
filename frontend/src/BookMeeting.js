import React, {useEffect, useReducer, useState} from 'react';
import {Calendar, momentLocalizer} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Container, Modal, Dropdown, Divider, Form, Message, Label, Popup, Header, List} from "semantic-ui-react";
import axios from 'axios';
import Select from 'react-select';
import './BookMeeting.css';

import CONFIG from './config';
import { parseFromDate } from './functions/DateChange';

const authDictionary = {
    "0": "Student",
    "1": "Professor",
    "2": "Department Staff"
}

//const invitee_url = CONFIG.URL + '/invitee';
const user_url = CONFIG.URL + '/users';
const roomAvail_url = CONFIG.URL + "/rooms/availability"
const available_url = CONFIG.URL + '/schedule/available';
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
    const [showEvent, setShowEvent] = useState(false); // boolean to show event popup modification
    const [appointedRoom, setAppointedRoom] = useState({}); // who appointed a room (user)
    const [allInvitees, setAllInvitees] = useState([]); // holds all invitees of selected event
    const [inviteeEmails, setInviteeEmails] = useState(""); // holds all invitee emails of selected event
    const [selectedInvitees, setSelectedInvitees] = useState([]); // holds all invitees of selected event
    const [invsToRmv, setInvsToRmv] = useState([]);
    const [rawSchedules, setRawSchedules] = useState([]); // get from r_unavail
    const [selectedRoom, setSelectedRoom] = useState({'text': 'Select Room', 'value': -1});
    const [sucessText, setSucessText] = useState("");
    const [selectedEventID, setSelectedEventID] = useState();
    const [warningText, setWarningText] = useState("");
    const [newEventName, setNewEventName] = useState();
    const [newEventDesc, setNewEventDesc] = useState();
    const [newEventStartTime, setNewEventStartTime] = useState();
    const [newEventEndTime, setNewEventEndTime] = useState();
    const [newEventDate, setNewEventDate] = useState();
    const [emails, setEmails] = useState("");
    const [availableTimes, setAvailableTimes] = useState("");
    const [eventInvitees, setEventInvitees] = useState("");
    const [availableRooms, setAvailableRooms] = useState([]);
    const [roomOptions, setRoomOptions] = useState([]);
    const [currEvent, setCurrEvent] = useState("");
    const [showModify, setShowModify] = useState(false);
    const [eventNewInfo, setEventNewInfo] = useState({});

    useEffect(() => {
        setUserDates([]);
        setRoomOptions([]);

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
        axios({method: 'GET', url: user_url})
        .then((res) => {
            let email_list = []
            for(let i = 0; i < res.data.length; i++) {
                if(res.data[i].user_id == user.user_id) continue;
                email_list.push({
                    label: res.data[i].user_email,
                    value: res.data[i].user_id,
                })
            };
            setEmails(email_list);
        });
        axios({method: 'GET', url: room_url})
        .then((res) => {
            let room_list = []
            for(let i = 0; i < res.data.length; i++) {
                if(res.data[i].authorization_level <= user.authorization_level){
                    room_list.push({
                    label: res.data[i].room_name,
                    value: res.data[i].room_id,
                    //authorization_level: res.data[i].authorization_level,
                    })
                }
            };
            setAvailableRooms(room_list);
        });
    }, []);


    const handleSelectedEvent = (event) => {
        setWarningText("")
        setSelected(event);
        setShowEvent(true);
        setCurrEvent({});
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
                                setCurrEvent(allSchedules[i])
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
                let invs = []
                for (let i = 0; i < res.data.length; i++) {
                    if (i != res.data.length - 1) 
                        emailString += res.data[i].user_email + ", "
                    else
                        emailString += res.data[i].user_email
                    if (res.data[i].user_id != user.user_id)
                        invs.push({...res.data[i], label: res.data[i].user_email, value: res.data[i].user_id});
                }
                setInviteeEmails(emailString);
                setSelectedInvitees(invs);
            })
        }
        else{
            setAppointedRoom({
                user_first_name: user.first_name,
                user_last_name: user.last_name,
                user_id: user.user_id,
                user_email: user.user_email
            })
            setCurrEvent({
                schedule_name: 'Marked as busy',
                schedule_description: 'Marked as busy'
            })
        }
        
    }

    const modifyEvent = () =>{
        // Modify event would be modify schedule
        // Check if event is "scheduled = 0" aka "Marked as busy"
        // then check if schedule.user_id = logged_in_user.user_id
        setWarningText("");
        if (!currEvent.schedule_id)
            setWarningText("Cannot modify times marked as busy.");
        else if (currEvent.user_id != user.user_id)
            setWarningText("Cannot modify other people's schedules.");
        else {
            setShowEvent(false);
            setEventNewInfo({
                schedule_name: currEvent.schedule_name,
                schedule_description: currEvent.schedule_description
            })
            setShowModify(true);            
        }
    }

    const modifyEventSet = (event) => {
        if (event.target.name == 'event_name')
            setEventNewInfo({...eventNewInfo, schedule_name: event.target.value})
        else if (event.target.name == 'event_description')
            setEventNewInfo({...eventNewInfo, schedule_description: event.target.value})        
    }

    const modifyEventSubmit = () => {
        let sn = eventNewInfo.schedule_name;
        let sd = eventNewInfo.schedule_description;
        let new_event = {
            schedule_id: currEvent.schedule_id,
            schedule_name: sn ? sn : currEvent.schedule_name,
            schedule_description: sd ? sd : currEvent.schedule_description,            
            schedule_date: currEvent.schedule_date,
            schedule_start_time: currEvent.schedule_start_time,
            schedule_end_time: currEvent.schedule_end_time,
            room_id: currEvent.room_id,
            user_id: currEvent.user_id
        }
        
        axios({method: 'PUT', data: new_event, url: CONFIG.URL + '/schedule',
               headers: {'Content-Type': 'application/json'}})
        .then(() => {
            setShowModify(false);
            setTimeout(() => window.location.reload(), 1000);
        });
    }

    const deleteInvitees = () => {
        if (!invsToRmv || invsToRmv.length == 0){
            setShowModify(false);            
            setTimeout(() => window.location.reload(), 1500);
        }
        
        let toDelete = invsToRmv.pop().invitee_id;
        console.log(toDelete)

        axios({method: 'DELETE', url: CONFIG.URL + '/invitee/' + toDelete})
        .then((res) => {
            if (invsToRmv.length > 0)
                deleteInvitees();
            else {
                setShowModify(false);            
                setTimeout(() => window.location.reload(), 1500);
            }
        })
    }

    const deleteEvent = () => {
        setWarningText("");
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
            setShowEvent(false);
            setSucessText('Event deleted! Refreshing page...')
            setTimeout(function() {
                //reload page
                window.location.reload();
            }, 2500);
        })
        .catch((err) => console.log(err))
        setWarningText("Your are not host of event.")
    }

    const markTime = () => {
            if (dates.length >= 1) {
                setWarningText("");
                let start = dates[0].start.toString();
                let end = dates[0].end.toString();
                console.log(start, end);
                let parsed = parseFromDate(start, end)
                console.log(parsed);
        
                let marking_slot = {
                    "user_id": user.user_id,
                    "user_date": parsed[0],
                    "user_start_time": parsed[1],
                    "user_end_time": parsed[2]
                }

                console.log(marking_slot);
                
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

    const getAvailableTimes = () =>{
        setAvailableTimes("")
        setWarningText("");
        let inv = "";
        for(let i = 0; i < eventInvitees.length; i++){
            inv += eventInvitees[i].value +",";        
        }
        inv += user.user_id.toString(); // inv = "3,4,5"
        // console.log(newEventDate)
        // console.log(inv);
        let param = {
            date : newEventDate,
            invitees : inv
        }
        axios({
            method: 'GET',
            params: param,
            url: available_url
        })
        .then((res) => {
            if (typeof res.data.available_time_slots !== 'string'){
                let str = ""
                for (let i = 0; i < res.data.available_time_slots.length; i++) {
                    if (i == res.data.available_time_slots.length - 1)
                        str += res.data.available_time_slots[i]
                    else
                        str += res.data.available_time_slots[i] + ', '
                }                    
                setAvailableTimes(str);
            }
            else 
                setAvailableTimes(res.data.available_time_slots);
            //console.log(res.data)
        })
        .catch((err) => setWarningText("Please recheck date is correct."))
    }

    const switchAvailableRoom = (selected) => {
        setSelectedRoom(selected);
        //setTimeout(() => {}, 250);
    }

    const makeEvent = () => {
        setWarningText("");
        setAvailableTimes("");
        let inv = [];
        for(let i = 0; i < eventInvitees.length; i++){
            inv.push(parseInt(eventInvitees[i].value));        
        }
        inv.push(user.user_id);
        // console.log(newEventDate);
        // console.log(newEventName.target.value);
        // console.log(newEventDesc.target.value);
        let data = {
            "schedule_start_time": newEventStartTime.target.value,
            "schedule_end_time": newEventEndTime.target.value,
            "schedule_date": newEventDate,
            "invitees": inv,
            "user_id": user.user_id,
            "room_id": selectedRoom.value,
            "schedule_name": newEventName.target.value,
            "schedule_description": newEventDesc.target.value
        }
        console.log(data);
        axios({
            method: 'POST',
            data: data,
            url: CONFIG.URL + "/schedule",
            headers: {'Content-Type': 'application/json'}
        })
        .then((res) => {
            setTimeout(() => {window.location.reload()}, 2500);
        })
        .catch((err)=>{
            console.log(err)
            setWarningText("Form is wrongly filled. Please check the information again.")
        })
    }

    const getAvailableRooms = () =>{
        let room_holder = [];
        let param = {
            date : newEventDate,
            start_time : newEventStartTime.target.value,
            end_time : newEventEndTime.target.value
        }
        axios({
            method: 'GET',
            params: param,
            url: roomAvail_url
        })
        .then((res) => {
            for(let i = 0; i < res.data.length; i++) {
                for(let j = 0; j < availableRooms.length; j++) {    
                    if(availableRooms[j].value == res.data[i].room_id) {
                        room_holder.push(availableRooms[j]);
                        break;
                    }
                }
            }
            setRoomOptions(room_holder);
        })
      
    }

    return (
    <Container style={{height:"800px"}}>
        <Container fluid style={{alignItems:"center", justifyContent:"center"}}>
            <Button 
                color = {'green'}
                onClick={() => {setOpen(true)}}
            > Book Meeting 
            </Button>
            <Button
                color={'black'}
                onClick={markTime}
            >Mark time as unavailable
            </Button>
        </Container>
        <Divider/>
        <Calendar
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
                marginTop:"5%",
            }}
            open={showEvent}
            dimmer={'blurring'}
            onClose={() => setShowEvent(false)}
            onOpen={() => setShowEvent(true)}
        >
            <Modal.Header>Event Information</Modal.Header>
                <Modal.Content>
                    <Modal.Description>
                        <Header>Event Name:</Header>
                        <code style={{color:"black"}}>
                            {
                                currEvent == {} ? "" : `${currEvent.schedule_name}`
                            }
                        </code>
                    </Modal.Description>
                    <Divider/>
                    <Modal.Description>
                        <Header>Event Description:</Header>
                        <code style={{color:"black"}}>
                            {
                                currEvent == {} ? "" : `${currEvent.schedule_description}`
                            }
                        </code>
                    </Modal.Description>
                    <Divider/>
                    <Modal.Description>
                        <Header>Scheduled by:</Header>
                        <code style={{color:"black"}}>
                            {    
                                appointedRoom.user_first_name + ' ' + appointedRoom.user_last_name
                            }   
                        </code>
                    </Modal.Description>
                    <Divider/>
                    <Modal.Description>
                        <Header>Invited users:</Header>
                        <List horizontal>
                            <List.Item as='a'>
                                {  
                                    inviteeEmails == "" ? "" : `${inviteeEmails}`
                                }
                            </List.Item>
                        </List>
                    </Modal.Description>
                </Modal.Content>
                <label className="warning">{warningText}</label>
                <Modal.Actions>
                    <Button onClick={modifyEvent} color="orange">Modify Event</Button>
                    <Button onClick={deleteEvent} color="red">Delete Event</Button>
                    <Button onClick={() => setShowEvent(false)} color="green">CLOSE</Button>
            </Modal.Actions>
        </Modal>


        <Modal
            centered={true}
            open={open}
            onClose={() => setOpen(false)}
            onOpen={() => setOpen(true)}
            style={{marginLeft:"15%"}}
            >
        <Modal.Header>
           Create Event
        </Modal.Header>
        <Modal.Content>
           
            <Form>
                <span className="warning">{warningText}</span>
                <span className="success">{sucessText}</span>
                <Form.Field>
                    <label>Name of Event</label>
                    <input type="text"
                        autoComplete="off"
                        onChange={setNewEventName} 
                        required 
                        placeholder="Name of Event" />
                </Form.Field>
                <Form.Field>
                    <label>Description of event</label>
                    <input type="text" 
                        autoComplete="off" 
                        onChange={setNewEventDesc}
                        required
                        placeholder="Description of Event"/>
                </Form.Field>
                <Form.Field>
                    <label>Users to invite</label>
                    <Select name="Rooms" 
                        class = "ui search dropdown"
                        search
                        isMulti = {true}
                        options={emails}
                        onChange = {(event) => {setEventInvitees(event)}}
                        style={{marginBottom: "1em"}}
                        placeholder="Select users to invite..."
                    />
                </Form.Field>
                <Form.Field>
                    <label>Date (YYYY-MM-DD)</label>
                    <input type="text"     
                        autoComplete="off"     
                        onChange={(event) => { setNewEventDate(event.target.value) }}
                        required />
                </Form.Field>
                        <Message>Invitees availability to event will be displayed once a date is chosen</Message>
                <Form.Field>
                <Popup
                    trigger=
                    {
                        <Button color={'orange'} onClick={getAvailableTimes}>
                            Get available times
                        </Button>
                    }
                    on='click'
                    content={<>{availableTimes}</>}
                    position='right center'
                    hideOnScroll
                        /> 
                </Form.Field>
                <Form.Field>
                    <label>Start Time (HH:MM:SS)</label>
                    <input type="text"
                        autoComplete="off" 
                        onChange={setNewEventStartTime} 
                        required
                        placeholder="Start Time"/>
                </Form.Field>
                <Form.Field>
                    <label>End Time (HH:MM:SS)</label>
                    <input type="text"
                        autoComplete="off"
                        onChange={setNewEventEndTime}
                        required
                        placeholder="End Time"/> 
                </Form.Field>
                <Message>Select data and timeframe for room options to be available.</Message>
                <Form.Field>
                    <Popup
                        trigger=
                        {
                            <Button
                                color={'orange'}
                                onClick={getAvailableRooms}>
                                    Get available rooms
                            </Button>
                        }
                        mouseEnterDelay={500}
                        mouseLeaveDelay={500}
                        on='click'
                        content={'Available rooms will show now...'}
                        positition='right center'
                        hideOnScroll
                    /> 
                </Form.Field>
                <Form.Field>
                    <label>Select a Room</label>
                    <Select name="Rooms" class = "ui search dropdown"
                        placeholder = "Select a Room"
                        search
                        options={roomOptions}
                        onChange={switchAvailableRoom}
                        style={{marginBottom: "1em"}}
                    />
                </Form.Field>
    
                <Form.Field>
                    <label className="warning">{warningText}</label>
                    <Button 
                        color="green"  
                        onClick={makeEvent}>
                        Create event
                    </Button>
                    <Button onClick={() => { setOpen(false); setWarningText("") }} 
                        color="grey"
                        >Close
                    </Button>
                </Form.Field>
            </Form>
        </Modal.Content>
    </Modal>

    <Modal
        style={{
            marginLeft: "15%",
            marginTop: "1%",
            height: "auto",
            padding:"1rem",
        }}
        open={showModify}
        dimmer={'blurring'}
        onClose={() => setShowModify(false)}
        onOpen={() => setShowModify(true)}
        >
        <Modal.Header>Modify Event</Modal.Header>
        <Modal.Content>
        <Form>
            <Form.Field>
                <label>Name of Event</label>
                <input type="text"
                    autoComplete="off"
                    name="event_name"
                    onChange={modifyEventSet}
                    value={eventNewInfo.schedule_name} 
                    required 
                    placeholder="Name of Event" />
            </Form.Field>
            <Form.Field>
                <label>Description of event</label>
                <input type="text" 
                    autoComplete="off"
                    name="event_description" 
                    onChange={modifyEventSet}
                    value={eventNewInfo.schedule_description}
                    required
                    placeholder="Description of Event"/>
            </Form.Field>
            <Form.Field>
                <Button onClick={modifyEventSubmit} color="orange">Modify Event</Button> 
            </Form.Field>
            <Message>Modify Event only modifies the event, does not delete invitees.</Message>            
            <Form.Field>
                <label>Invitees to remove</label>
                <Select name="Invitees" 
                    class = "ui search dropdown"
                    search
                    isMulti = {true}
                    options={selectedInvitees}
                    onChange = {(event) => {setInvsToRmv(event)}}
                    style={{marginBottom: "1em"}}
                    placeholder="Select users to invite..."
                />
            </Form.Field>
            <Form.Field>
                <Button onClick={deleteInvitees} color="red">DELETE INVITEES</Button>
                <Button onClick={() => setShowModify(false)} color="grey">CLOSE</Button>
            </Form.Field>
            <Message>Delete Invitees deletes invitees only.</Message> 
        </Form>
        </Modal.Content>
    </Modal>
    </Container >
    );
}
export default BookMeeting;
