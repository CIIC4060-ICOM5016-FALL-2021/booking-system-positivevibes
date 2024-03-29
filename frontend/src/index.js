import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import {Route, Navigate, BrowserRouter, Routes} from 'react-router-dom';
import HomePage from "./HomePage";
import 'semantic-ui-css/semantic.min.css'
import UserView from "./UserView";
import Dashboard from "./Dashboard";

ReactDOM.render(
    <BrowserRouter>
        <Routes>
            <Route exact path="/Home" element={<HomePage/>} />
            <Route exact path="/UserView" element={<UserView/>} />
            <Route exact path="/Dashboard" element={<Dashboard/>} />
            <Route path="*" element={<Navigate to ="/Home" />}/>
        </Routes>
    </BrowserRouter>,
    document.getElementById('root')
);
