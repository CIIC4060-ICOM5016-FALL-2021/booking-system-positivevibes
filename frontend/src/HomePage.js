import React, {Component, useState} from 'react';
import {Button, Divider, Form, Grid, Header, Modal, Segment, Tab} from 'semantic-ui-react';
import CONFIG from './config';
// import axios from 'axios';


function HomePage() {
    const [open, setOpen] = useState(false);
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    console.log(open);

    const handleChange = (event, newValue) => {
        // setOpen(true);
        console.log(event.target)
        if (event.target.type == 'email')
            setEmail(newValue)
        else if (event.target.type == 'password')
            setPassword(newValue)
        
    }

    const logMe = () => {
        console.log("Email: ", email.value)
        console.log("Password: ", password.value)
    }

    const login = () => {
        let body = {
            "room_id" : "4",
            "user_id" : "14",
            "date" : "2021-11-16",
            "time" : "13:30:00"
        }
        let url = CONFIG.URL+'/rooms'

        console.log(JSON.stringify(body))
        console.log("URL: ", url)

        fetch(url, {method: 'GET'})
        .then((res) => res.json())
        .then((json) => console.log(json))

        // axios({
        //     method: 'get',
        //     url: url,
        //     headers: {
        //         "Access-Control-Allow-Origin": '*'
        //     }
        // })

        // axios({
        //     method: 'get',
        //     url: url,
        //     headers: {
        //         "Access-Control-Allow-Origin": true
        //     }
        //     // data: JSON.stringify(body)
        // })
        // .then((res) => console.log(res))

        // fetch(CONFIG.URL+'/rooms/appointed', {
        //     method: 'GET',
        //     headers: {
        //         'Content-Type': 'application/json'
        //     },
        //     body: JSON.stringify(body)
        // })
        // .then((res) => res.json())
        // .then((json) => {
        //     console.log(json)
        // })
        // let result = response.items()
        // console.log(response)
    }

    return (<Segment><Header dividing textAlign="center" size="huge">Welcome to PosVibesDB</Header>
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
                                placeholder='•••••'
                                type='password'
                                onChange={handleChange}
                            />
                            <Button content='Login' primary onClick={login}/>
                        </Form>
                    </Grid.Column>
                    <Grid.Column verticalAlign='middle'>
                        <Button content='Sign up' icon='signup' size='big' onClick={handleChange}/>
                    </Grid.Column>
                </Grid>

                <Divider vertical>Or</Divider>
            </Segment>
        </Segment>
    )
}


export default HomePage;
