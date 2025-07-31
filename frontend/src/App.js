/**
 * This is the main component of the application.
 * It sets up the routing and navigation for the entire app.
 */
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

import AuthService from './services/AuthService';
import Login from './components/Login';
import Register from './components/Register';
import Logout from './components/Logout';
import Dashboard from './components/Dashboard';
import Home from './components/Home';
import Book from './components/Book';
// Import your other components here
// import Profile from './components/Profile';
// import AdminDashboard from './components/AdminDashboard';

const App = () => {
  // Get the current user from the AuthService
  const currentUser = AuthService.getCurrentUser();

  return (
    <Router>
      <div>
        <nav className="navbar navbar-expand navbar-dark bg-dark">
          <Link to={'/'} className="navbar-brand">
            Silent Library
          </Link>
          <div className="navbar-nav mr-auto">
            <li className="nav-item">
              <Link to={'/home'} className="nav-link">
                Home
              </Link>
            </li>

            {/* Show the dashboard link only if the user is logged in */}
            {currentUser && (
              <li className="nav-item">
                <Link to={'/dashboard'} className="nav-link">
                  Dashboard
                </Link>
              </li>
            )}

            {/* Show the admin dashboard link only if the user is an admin */}
            {currentUser && currentUser.is_staff && (
              <li className="nav-item">
                <Link to={'/admin'} className="nav-link">
                  Admin Dashboard
                </Link>
              </li>
            )}
          </div>

          {/* Show the user's profile and logout links if the user is logged in */}
          {currentUser ? (
            <div className="navbar-nav ml-auto">
              <li className="nav-item">
                <Link to={'/profile'} className="nav-link">
                  {currentUser.username}
                </Link>
              </li>
              <li className="nav-item">
                <a href="/logout" className="nav-link" onClick={Logout}>
                  Logout
                </a>
              </li>
            </div>
          ) : (
            // Show the login and sign up links if the user is not logged in
            <div className="navbar-nav ml-auto">
              <li className="nav-item">
                <Link to={'/login'} className="nav-link">
                  Login
                </Link>
              </li>

              <li className="nav-item">
                <Link to={'/register'} className="nav-link">
                  Sign Up
                </Link>
              </li>
            </div>
          )}
        </nav>

        <div className="container mt-3">
          {/* Define the routes for the application */}
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/home" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/logout" element={<Logout />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/book/:id" element={<Book />} />
            {/* <Route path="/profile" element={<Profile />} />
            <Route path="/admin" element={<AdminDashboard />} /> */}
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
