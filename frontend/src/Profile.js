import React, { Component, useEffect, useState } from 'react';
import { Button, Popup, Table, Icon, Input, Segment, Container } from 'semantic-ui-react';
import axios from 'axios';
import CONFIG from './config';

function Profile() {
    const user = JSON.parse(localStorage.getItem('User'));
    const [visible, setVisibility] = useState(false);
    const [passwordShown, setPasswordShown] = useState(false);

    const [uFirstName, setUFirstName] = useState('');
    const [uLastName, setULastName] = useState('');
    const [uEmail, setUEmail] = useState('');
    const [uPassword, setUPassword] = useState('');

    const dictionary = {
        "0": "Student",
        "1": "Professor",
        "2": "Department Staff"
    };

    const auth_lvl = dictionary[user.authorization_level.toString()];
    const url = CONFIG.URL + '/users'

     const togglePasswordVisiblity = () => {
         setPasswordShown(passwordShown ? false : true);
    };

    const inputField = (event) => {
        console.log(event.target.name);
        console.log(event.target.value);
        switch (event.target.name) {
            case 'firstName':
                setUFirstName(event.target.value);
            case 'lastName':
                setULastName(event.target.value);
            case 'uEmail':
                setUEmail(event.target.value);
            case 'uPassword':
                setUPassword(event.target.value);
            default:
                break;
        }
    }

    const changeFirstName = () => {
        let newUser = {
            user_id: user.user_id,
            first_name: uFirstName,
            last_name: user.last_name,
            authorization_level: user.authorization_level,
            user_email: user.user_email,
            user_password: user.user_password
        }
        console.log("New User", newUser);
        axios({
            method: 'PUT',
            url: url,
            data: newUser,
            headers: {'Content-Type': 'application/json'}
        })
        .then((res) => {
            localStorage.setItem('User', JSON.stringify(res.data))
            setTimeout(() => window.location.reload(), 2500);
        });
    };
    
    const changeLastName = () => {
        let newUser = {
            user_id: user.user_id,
            first_name: user.first_name,
            last_name: uLastName,
            authorization_level: user.authorization_level,
            user_email: user.user_email,
            user_password: user.user_password
        }
        console.log("New User", newUser);
        axios({
            method: 'PUT',
            url: url,
            data: newUser,
            headers: {'Content-Type': 'application/json'}
        })
        .then((res) => {
            localStorage.setItem('User', JSON.stringify(res.data))
            setTimeout(() => window.location.reload(), 2500);
        });
    };
    
    const changeEmail = () => {
        let newUser = {
            user_id: user.user_id,
            first_name: user.first_name,
            last_name: user.last_name,
            authorization_level: user.authorization_level,
            user_email: uEmail,
            user_password: user.user_password
        }
        console.log("New User", newUser);
        axios({
            method: 'PUT',
            url: url,
            data: newUser,
            headers: {'Content-Type': 'application/json'}
        })
        .then((res) => {
            localStorage.setItem('User', JSON.stringify(res.data))
            setTimeout(() => window.location.reload(), 2500);
        });
    };

    const changePassword = () => {
        let newUser = {
            user_id: user.user_id,
            first_name: user.first_name,
            last_name: user.last_name,
            authorization_level: user.authorization_level,
            user_email: user.user_email,
            user_password: uPassword,
        }
        console.log("New User", newUser);
        axios({
            method: 'PUT',
            url: url,
            data: newUser,
            headers: {'Content-Type': 'application/json'}
        })
        .then((res) => {
            localStorage.setItem('User', JSON.stringify(res.data))
            setTimeout(() => window.location.reload(), 2500);
        });
    };

     
    return (
        <>
            <Container style={{alignItems:"center", justifyContent:"center", padding:"2rem"}}>
                <Segment color={'teal'}
                    compact
                    inverted
                >
                    Click on the green buttons to edit the user information
                </Segment>
                <Button color={'red'}>Delete user?</Button>
            <Table color={'violet'} inverted compact celled collapsing textAlign={"center"}>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell>
                            <Button color={'violet'}>
                                Occupation
                            </Button>
                        </Table.HeaderCell>
                        <Popup
                            content={
                                <Input
                                    icon={<Icon name='check circle'  
                                        inverted
                                        circular
                                        link
                                        onClick={changeFirstName} 
                                        />
                                    }
                                    name="firstName"
                                    onChange={inputField}
                                    placeholder='New first name'
                                    type='text'
                                />
                            }
                            on='click'
                            position='bottom center'
                            pinned
                            offset={[0, 50]}
                            trigger={<Table.HeaderCell>
                                <Button color={'green'}>
                                    First Name
                                </Button>
                            </Table.HeaderCell>
                            }
                        />
                        
                        <Popup
                            content={
                                <Input
                                    icon={<Icon name='check circle'
                                        inverted
                                        circular 
                                        link 
                                        onClick={changeLastName}
                                    />
                                    }
                                    name="lastName"
                                    onChange={inputField}
                                    placeholder='New last name'
                                />
                            }
                            on='click'
                            position='bottom center'
                            pinned
                            offset={[0, 50]}
                            trigger={<Table.HeaderCell>
                                <Button color={'green'}>
                                    Last Name
                                </Button>
                            </Table.HeaderCell>
                            }
                        />
                       
                        <Popup
                            content={
                                <Input
                                    icon={<Icon name='check circle'  
                                        inverted
                                        circular 
                                        link
                                        onClick={changeEmail} 
                                    />
                                    }
                                    name="uEmail"
                                    onChange={inputField}
                                    placeholder='New Email'
                                />
                            }
                            on='click'
                            position='bottom center'
                            pinned
                            offset={[0, 50]}
                            trigger={<Table.HeaderCell>
                                <Button color={'green'}>
                                    Email
                                </Button>
                            </Table.HeaderCell>
                            }
                        />
                        
                        <Popup
                            content={
                                <Input
                                    icon={<Icon name='check circle'  
                                        inverted
                                        circular 
                                        link
                                        onClick={changePassword} 
                                    />
                                    }
                                    name="uPassword"
                                    onChange={inputField}
                                    placeholder='New Password'
                                />
                            }
                            on='click'
                            position='bottom center'
                            pinned
                            offset={[0, 50]}
                            trigger={<Table.HeaderCell>
                                <Button color={'green'}>
                                    Password
                                </Button>
                            </Table.HeaderCell>
                            }
                        />
                    </Table.Row>
                </Table.Header>

                <Table.Body>
                    <Table.Row>
                        <Table.Cell>{auth_lvl}</Table.Cell>
                        <Table.Cell>{user.first_name}</Table.Cell>
                        <Table.Cell>{user.last_name}</Table.Cell>
                        <Table.Cell>{user.user_email}</Table.Cell>
                        <Table.Cell>
                            {passwordShown ? user.user_password : "••••••••"}
                            <i class={passwordShown ? "eye icon" : "eye slash icon"} onClick={() => setPasswordShown(!passwordShown)}></i>
                        </Table.Cell>
                    </Table.Row>
                </Table.Body>
                </Table>
                </Container>
        </>
    );
}

export default Profile;