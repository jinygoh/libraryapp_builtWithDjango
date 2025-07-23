// This component renders the login page of the application.
// It contains a form for users to enter their credentials and log in.

import React, { useState } from 'react';
// Import the pre-configured axios instance.
import axios from '../axios';
// Import the useNavigate hook from react-router-dom for navigation.
import { useNavigate } from 'react-router-dom';

const Login = () => {
    // Use the useState hook to manage the state of the username and password fields.
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    // Use the useNavigate hook to get the navigation function.
    const navigate = useNavigate();

    // This function is called when the form is submitted.
    const handleSubmit = async (e) => {
        // Prevent the default form submission behavior.
        e.preventDefault();
        try {
            // Make a POST request to the /authenticate endpoint with the user's credentials.
            const response = await axios.post('/authenticate', { username, password });
            // If the authentication is successful, store the JWT in local storage.
            localStorage.setItem('token', response.data.jwt);
            // Navigate to the dashboard page.
            navigate('/dashboard');
        } catch (error) {
            // If the authentication fails, log the error to the console.
            console.error('Error logging in', error);
        }
    };

    return (
        <div>
            <h2>Login</h2>
            {/* The form calls the handleSubmit function when it is submitted. */}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username</label>
                    {/* The input field for the username is bound to the username state variable. */}
                    <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
                </div>
                <div>
                    <label>Password</label>
                    {/* The input field for the password is bound to the password state variable. */}
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                </div>
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default Login;
