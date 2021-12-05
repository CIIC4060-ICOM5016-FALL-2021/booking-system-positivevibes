import React, { Component, useEffect, useState } from 'react';
import { Button } from 'semantic-ui-react';
import { Table } from 'semantic-ui-react';
import { Icon } from 'semantic-ui-react'


function Profile() {
    const user = JSON.parse(localStorage.getItem('User'));
    const [visible, setVisibility] = useState(false);

    const dictionary = {
        "0": "Student",
        "1": "Professor",
        "2": "Department Staff"
    }

    let auth_lvl = dictionary[user.authorization_level.toString()]

    const usePasswordToggle = () => {
        const [visible, setVisibility] = useState(false);
        const InputType = visible ? "text" : "password";
        return [InputType, Icon];
    };
     
    return (
        <>
            <Table color={'violet'} inverted compact celled collapsing textAlign={"center"} style={{marginLeft:"20%"}}>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell>Occupation</Table.HeaderCell>
                        <Table.HeaderCell>First Name</Table.HeaderCell>
                        <Table.HeaderCell>Last Name</Table.HeaderCell>
                        <Table.HeaderCell>Email</Table.HeaderCell>
                        <Table.HeaderCell>Password</Table.HeaderCell>
                    </Table.Row>
                </Table.Header>

                <Table.Body>
                    <Table.Row>
                        <Table.Cell>{auth_lvl}</Table.Cell>
                        <Table.Cell>{user.first_name}</Table.Cell>
                        <Table.Cell>{user.last_name}</Table.Cell>
                        <Table.Cell>{user.user_email}</Table.Cell>
                        <script>
                            if (visible) {
                                <Table.Cell icon={"eye"}
                                >{user.user_password}</Table.Cell>
                            }
                            else {
                                <Table.Cell icon={"eye-slash"}
                                >••••••••</Table.Cell>
                            }
                        </script>                        
                    </Table.Row>
                </Table.Body>
            </Table>
        </>
    );
}

export default Profile;