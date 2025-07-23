// This component renders the header for the application.
// It contains links to the different pages of the application.

import React from 'react';
// Import the Link component from react-router-dom for creating links.
import { Link } from 'react-router-dom';

const Header = () => {
    return (
        <header>
            <nav>
                <ul>
                    {/* The Link component creates a link to the specified page. */}
                    <li><Link to="/">Home</Link></li>
                    <li><Link to="/login">Login</Link></li>
                    <li><Link to="/register">Register</Link></li>
                    <li><Link to="/dashboard">Dashboard</Link></li>
                    <li><Link to="/admin">Admin</Link></li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;
