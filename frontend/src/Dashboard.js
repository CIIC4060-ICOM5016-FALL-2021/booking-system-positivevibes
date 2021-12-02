import React from 'react';
import {Tab} from "semantic-ui-react";

import GlobalStats from './GlobalStats';
import LogOut from './LogOut';

function Dashboard(){
    const panes = [
        {
            menuItem: 'Global Statistics', render: () => <GlobalStats/>
        },
        {
            menuItem: 'User View', render: () => {window.location.href = window.location.origin + '/UserView'}
        },
        {
            menuItem: 'Log out', render: () => <LogOut/>
        }
    ]

    panes.push()

    return <Tab panes={panes}/>
}

export default Dashboard;
