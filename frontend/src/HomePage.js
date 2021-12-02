import React, {Component, useState} from 'react';
import {Button, Divider, Form, Grid, Header, Modal, Segment, Tab} from 'semantic-ui-react';
import {Route, Navigate, BrowserRouter, Routes} from 'react-router-dom';
import CONFIG from './config';
import axios from 'axios';

import SignUp from './SignUp';

function HomePage() {
    const [open, setOpen] = useState(false);
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    // console.log(open);

    if (localStorage.getItem('User')) {
        return(
            <Navigate to="/UserView"/>
        )
    }

    const toggleSignUp = () => {
        setOpen(!open);
    }

    const handleChange = (event, newValue) => {
        // setOpen(true);
        // console.log(event.target)
        if (event.target.type == 'email')
            setEmail(newValue)
        else if (event.target.type == 'password')
            setPassword(newValue)
    }

    const login = () => {
        if (localStorage.getItem('User')) {
            console.log("User already logged in.")
            console.log(JSON.parse(localStorage.getItem('User')))
            return
        }

        let url = CONFIG.URL+'/users'

        axios({
            method: 'GET',
            url: url
        })
        .then((res) => {
            let data = res.data

            // we have all users, check if email exists within them
            for (let i = 0; i < data.length; i++) {
                if (data[i]['user_email'] == email.value) {
                    if (data[i]['user_password'] == password.value){
                        localStorage.setItem('User', JSON.stringify(data[i]))
                        console.log("Matched: ", data[i])
                        break
                    }
                    else{
                        console.log("Password doesn't match.")
                        break
                    }
                }
                if (i == data.length - 1)
                    console.log("Email not found.")   
            }
                
            if (!localStorage.getItem('User'))
                console.log("Login failed.")
            else{
                console.log("Login successful.")
                window.location.href = window.location.origin+"/UserView"
            }
        })
        
    }

    const redirectMe = () => {
        // <a href= {window.location.origin+"/UserView"}/>
        // <meta http-equiv="Refresh" content={"0; url="+window.location.origin+"/UserView"} />
        // console.log(window.location.origin+"/UserView")
        window.location.href = window.location.origin+"/UserView"
    }

    return (<Segment><Header dividing textAlign="center" size="huge">Welcome to PosVibesDB</Header>
            <Modal
                centered={true}
                open={open}
                onClose={() => setOpen(false)}
                onOpen={() => setOpen(true)}
            >
                {/* <Modal.Header>Sign Up Form</Modal.Header> */}
                <Modal.Content>
                    <SignUp></SignUp>
                    {/* <Modal.Description>
                        This is a modal but it serves to show how buttons and functions can be implemented.
                    </Modal.Description> */}
                </Modal.Content>
                <Modal.Actions>
                    <Button onClick={() => setOpen(false)}>CLOSE</Button>
                </Modal.Actions>
            </Modal>
            <Segment placeholder>

                <Grid columns={2} relaxed='very' stackable>
                    <Grid.Column>
                        <Form>
                            <Form.Input
                                icon='user'
                                iconPosition='left'
                                label='Email'
                                placeholder='Email'
                                type='email'
                                onChange={handleChange}
                            />
                            <Form.Input
                                icon='lock'
                                iconPosition='left'
                                label='Password'
                                placeholder='••••••••'
                                type='password'
                                onChange={handleChange}
                            />
                            <Button content='Login' primary onClick={login}/>
                        </Form>
                    </Grid.Column>
                    <Grid.Column verticalAlign='middle'>
                        <Button content='Sign up' icon='signup' size='big' onClick={toggleSignUp}/>
                    </Grid.Column>
                </Grid>

                <Divider vertical>Or</Divider>
            </Segment>
        </Segment>
    )
}


export default HomePage;
