import {useState} from 'react';
import Select from 'react-select';
import 'bootstrap/dist/css/bootstrap.min.css';
import CONFIG from './config';
import axios from 'axios';

import './SignUp.css';

function SignUp() {
    const url = CONFIG.URL + '/users';
    const passwordType = 'password';
    const [password,setPassword] = useState(passwordType);
    
    const passwordEye = 'fa fa-eye-slash';
    const [eye,setEye] = useState(passwordEye);
    
    const EyeChange = () =>{
        if(password=='password') {
            setPassword("text");
            setEye("fa fa-eye");
        }
        else {
            setPassword("password");
            setEye("fa fa-eye-slash");
        }    
    }
    
    const [warningText, setWarningText] = useState("");
    const [sucessText, setSucessText] = useState("");
    const [name, setName] = useState("");
    const [lastName, setLastName] = useState("");
    const [email_input, setEmail_input] = useState("");
    const [password_input, setPassword_input] = useState("");
    const [authLevel, setAuthLevel] = useState({});
    const authorizations = [
        {label: "Student", value: 0},
        {label: "Professor", value: 1},
        {label: "Department Staff", value: 2}
    ];
    
    const InputText = (event) => {
        setName(event.target.value);
    }

    const InputLastName = (event) => {
        setLastName(event.target.value);
    }
    
    const InputEmail = (event) => {
        setEmail_input(event.target.value);
    }
    
    const InputPassword = (event) => {
        setPassword_input(event.target.value);
    }

    const InputAuthLevel = (event) => {
        setAuthLevel(event);
    }
    
    const SubmitForm =(e)=>{
        e.preventDefault();
        if(name && lastName && email_input && password_input
            && authLevel){
            let user = {
                first_name: name,
                last_name: lastName,
                user_email: email_input,
                user_password: password_input,
                authorization_level: authLevel.value
            };
            // console.log(user);

            // fetch(url, {
            //     method: 'POST',
            //     body: JSON.stringify(user),
            //     headers: {
            //         'Content-Type': 'application/json'
            //     }
            // })
            // .then((res) => res.json())
            // .then((data) => {
            //     setWarningText("");
            //     setName("");
            //     setLastName("");
            //     setEmail_input("");
            //     setPassword_input("");
            //     setAuthLevel({});
            //     console.log(data);
            //     setSucessText("User signed up!");
            //     // alert("Form Submitted");
            // });

            axios({
                method: 'POST',
                url: url,
                data: user,
                headers: {'Content-Type': 'application/json'}
            })
            .then((res) => {
                setWarningText("");
                setName("");
                setLastName("");
                setEmail_input("");
                setPassword_input("");
                setAuthLevel({});
                console.log(res);
                setSucessText("User signed up!");
                // alert("Form Submitted");
            })

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
                    <h4>Create an Account</h4>
                    <span className="warning">{warningText}</span>
                    <span className="success">{sucessText}</span>
                </div>
                <div className="input_field">
                    <input type="text" onChange={InputText} value={name} required />
                    <span>First Name</span>
    
                </div>
                <div className="input_field">
                    <input type="text" onChange={InputLastName} value={lastName} required />
                    <span>Last Name</span>
    
                </div>
                <div className="input_field">
                    <input type="text" required autoComplete="off" onChange={InputEmail} value={email_input} />
                    <span>Email</span>
                </div>
                <div className="input_field">
                    <input type={password} autoComplete="off" onChange={InputPassword} value={password_input} required />
                    <span>Password</span>
                    <small onClick={EyeChange}><i className={eye}></i></small>
                </div>
    
                <div className="input_field">
                    <div className="container">
                        <div className="row">
                        <div className="col-lg-auto"></div>
                        <div className="col-lg-auto">
                            <Select options={authorizations} onChange={InputAuthLevel}/>
                        </div>
                        <div className="col-lg-auto"></div>
                        </div>
                    </div>
                </div>
    
                <div className="submit_button">
                    <button onClick={SubmitForm}>Signup</button>
                </div>
    
            </div>
        </div>
    </>
    );
    
    }
    
export default SignUp;