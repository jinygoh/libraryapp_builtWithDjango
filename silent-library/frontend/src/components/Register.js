// This component renders the registration page of the application.
// It contains a form for users to enter their information and register a new account.

import React, { useState } from 'react';
// Import the pre-configured axios instance.
import axios from '../axios';
// Import the useNavigate hook from react-router-dom for navigation.
import { useNavigate } from 'react-router-dom';

const Register = () => {
    // Use the useState hook to manage the state of the form fields.
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    // Use the useNavigate hook to get the navigation function.
    const navigate = useNavigate();

    // This function is called when the form is submitted.
    const handleSubmit = async (e) => {
        // Prevent the default form submission behavior.
        e.preventDefault();
        try {
            // Make a POST request to the /register endpoint with the user's information.
            await axios.post('/register', { username, password, email, firstName, lastName });
            // If the registration is successful, navigate to the login page.
            navigate('/login');
        } catch (error) {
            // If the registration fails, log the error to the console.
            console.error('Error registering', error);
        }
    };

    return (
        <div>
            <h2>Register</h2>
            {/* The form calls the handleSubmit function when it is submitted. */}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username</label>
                    {/* The input fields are bound to their respective state variables. */}
                    <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
                </div>
                <div>
                    <label>Password</label>
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                </div>
                <div>
                    <label>Email</label>
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                </div>
                <div>
                    <label>First Name</label>
                    <input type="text" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
                </div>
                <div>
                    <label>Last Name</label>
                    <input type="text" value={lastName} onChange={(e) => setLastName(e.target.value)} />
                </div>
                <button type="submit">Register</button>
            </form>
        </div>
    );
};

export default Register;
