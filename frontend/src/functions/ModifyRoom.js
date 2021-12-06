import {useState, useEffect} from 'react';
import Select from 'react-select';
import 'bootstrap/dist/css/bootstrap.min.css';
import CONFIG from '../config';
import axios from 'axios';
import {Button} from "semantic-ui-react";

import './AddRoom.css';

function ModifyRoom() {
    const room_url = CONFIG.URL + '/rooms';
    const building_url = CONFIG.URL + '/buildings';
    
    const [warningText, setWarningText] = useState("");
    const [sucessText, setSucessText] = useState("");
    const [roomCapacity, setCapacity] = useState("");
    const [AuthLevel, setAuthLevel] = useState("");
    const [buildingId, setBuildingId] = useState("");
    const [roomName, setRoomName] = useState("");
    const [selectedRoom, setSelectedRoom] = useState("");
    const [buildings, setBuildings] = useState([]);
    const [rID, setRID] = useState();
    const [rooms, setRooms] = useState([]);
    const [buildingDict, setBuildingDict] = useState({});
    const authorizations = [
        {label: "Student", value: 0},
        {label: "Professor", value: 1},
        {label: "Department Staff", value: 2}
    ];
    const authDictionary = {
        "0": "Student",
        "1": "Professor",
        "2": "Department Staff"
    }

    const changeSelectedRoom = () => {
        setRoomName(selectedRoom.label);
        setAuthLevel(selectedRoom.authorization_level);
        setBuildingId(selectedRoom.building_id);
        setCapacity(selectedRoom.room_capacity);
    }
    
    const InputCapacity = (event) => {
        setCapacity(event.target.value);
    }

    const InputID = (event) => {
        setRID(event.value);
        setSelectedRoom(event);
    }

    const InputAuthLevel = (event) => {
        setAuthLevel(event.value);
    }
    
    const InputBuildingId = (event) => {
        setBuildingId(event.value);
    }
    
    const InputName = (event) => {
        setRoomName(event.target.value);
    }

    // const switchRoom = () => {
    //     //setSelectedRoom(selected);
    //     setRID(event.value);
    // }
    
    useEffect(() => {
        axios({
            method: 'GET',
            url: building_url
        })
        .then((res) => {
            let building_list = []
            let buildDict = {}
            for(let i = 0; i < res.data.length; i++) {
                building_list.push({
                    label: res.data[i].building_name,
                    value: res.data[i].building_id
                })
                buildDict[res.data[i].building_id.toString()] = res.data[i].building_name;
            };
            setBuildings(building_list);
            setBuildingDict(buildDict);
        });
        axios({
            method: 'GET',
            url: room_url
        })
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
    }, []);

    //(room_capacity, authorization_level, building_id, room_name)
    const modifyRoom = () => {        
        if (selectedRoom != "") {
            if(roomCapacity == ""){
                setCapacity(selectedRoom.room_capacity)
            }
            if(AuthLevel == ""){
                setAuthLevel(selectedRoom.authorization_level)
            }
            if(buildingId == ""){
                setBuildingId(selectedRoom.building_id)
            }
            if(roomName == ""){
                setRoomName(selectedRoom.room_name)
            }

            let room = {
                room_capacity: roomCapacity,
                authorization_level: AuthLevel,
                building_id: buildingId,
                room_name: roomName,
                room_id: rID,
            };
            axios({
                method: 'PUT',
                url: room_url,
                data: room,
                headers: {'Content-Type': 'application/json'}
            })
            .then((res) => {
                setWarningText("");
                setCapacity("");
                setAuthLevel("");
                setBuildingId("");
                setRoomName("");
                console.log(res);
                setSucessText("Room modified!");
            })

            setTimeout(function() {
                //reload page
                window.location.reload();
            }, 2500);
        }
        else{
            setWarningText("Please select a room to modify.");
        }
    }
    
    return(
    <>
        <div className="wrapper">
            <div className="card">
                <div className="heading">
                    <h4>Modify Room</h4>
                    <span className="warning">{warningText}</span>
                    <span className="success">{sucessText}</span>
                </div>
                <div className="input_field">
                    <div className="container">
                        <div className="col">
                        <div className="col-lg-auto"></div>
                        <div className="col-lg-auto">
                            <Select placeholder="Room to Modify" options={rooms} onChange={InputID}/>
                            <Button color={'blue'} onClick={changeSelectedRoom}>Select Room</Button>
                        </div>
                        <div className="col-lg-auto"></div>
                        </div>
                        </div>
                </div>
                <div className="input_field">
                    <input type="text" onChange={InputName} value={roomName} required />
                    <span>Room Name</span>
                </div>
                <div className="input_field">
                    <input type="number" onChange={InputCapacity} value={roomCapacity} required />
                    <span>Room Capacity</span>
                </div>
                <div className="input_field">
                    <div className="container">
                        <div className="col">
                        <div className="col-lg-auto"></div>
                        <div className="col-lg-auto">
                            <Select placeholder="Building Name" options={buildings} onChange={InputBuildingId}/>
                        </div>
                        <div className="col-lg-auto"></div>
                        </div>
                        </div>
                </div>
                <div className="input_field">
                    <div className="container">
                        <div className="col">
                        <div className="col-lg-auto"></div>
                        <div className="col-lg-auto">
                            <Select placeholder="Authorization Level" options={authorizations} onChange={InputAuthLevel}/>
                        </div>
                        <div className="col-lg-auto"></div>
                        </div>
                    </div>
                </div>

                <div className="submit_button">
                    <button 
                    color="green" 
                    onClick={modifyRoom}>Modify Room</button>
                </div>

            </div>
        </div>
    </>
    );
}
    
export default ModifyRoom;