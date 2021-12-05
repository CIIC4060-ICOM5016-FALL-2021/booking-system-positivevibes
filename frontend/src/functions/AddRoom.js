import {useState, useEffect} from 'react';
import Select from 'react-select';
import 'bootstrap/dist/css/bootstrap.min.css';
import CONFIG from '../config';
import axios from 'axios';

import './AddRoom.css';

function AddRoom() {
    const room_url = CONFIG.URL + '/rooms';
    const building_url = CONFIG.URL + '/buildings';
    
    const [warningText, setWarningText] = useState("");
    const [sucessText, setSucessText] = useState("");
    const [roomCapacity, setCapacity] = useState("");
    const [AuthLevel, setAuthLevel] = useState("");
    const [buildingId, setBuildingId] = useState("");
    const [roomName, setRoomName] = useState("");
    const [buildings, setBuildings] = useState([]);
    const authorizations = [
        {label: "Student", value: 0},
        {label: "Professor", value: 1},
        {label: "Department Staff", value: 2}
    ];
    
    const InputCapacity = (event) => {
        setCapacity(event.target.value);
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
    
    useEffect(() => {
        axios({
            method: 'GET',
            url: building_url
        })
        .then((res) => {
            let building_list = []
            for(let i = 0; i < res.data.length; i++) {
                building_list.push({
                    label: res.data[i].building_name,
                    value: res.data[i].building_id
                })
            };
            setBuildings(building_list);
        });
    }, []);

    //(room_capacity, authorization_level, building_id, room_name)
    const addRoom = () => {
        console.log("Building ID: \n")
        console.log(buildingId)
        console.log("Auth : \n")
        console.log(AuthLevel)
        if(roomCapacity && AuthLevel && buildingId && roomName){
            let room = {
                room_capacity: roomCapacity,
                authorization_level: AuthLevel,
                building_id: buildingId,
                room_name: roomName,
            };

            axios({
                method: 'POST',
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
                setSucessText("Room added!");
            })

            setTimeout(function() {
                //reload page
                window.location.reload();
            }, 2000);

        }
        else{
            setWarningText("All Fields are compulsory");
        }
    }
    
    return(
    <>
        <div className="wrapper">
            <div className="card">
                <div className="heading">
                    <h4>Create Room</h4>
                    <span className="warning">{warningText}</span>
                    <span className="success">{sucessText}</span>
                </div>
                <div className="input_field">
                    <input type="text"autoComplete="off" onChange={InputName} value={roomName} required />
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
                    onClick={addRoom}>Add Room</button>
                </div>
    
            </div>
        </div>
    </>
    );
    
    }
    
export default AddRoom;