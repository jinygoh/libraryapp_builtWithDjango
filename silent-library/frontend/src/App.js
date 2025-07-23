// This is the main component of the React application.
// It sets up the routing for the application and renders the other components.

import React from 'react';
// Import the necessary components from react-router-dom for routing.
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
// Import the other components.
import Header from './components/Header';
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import AdminDashboard from './components/AdminDashboard';
import BookList from './components/BookList';
import BookDetail from './components/BookDetail';
import Search from './components/Search';

function App() {
  return (
    // The Router component provides the routing functionality.
    <Router>
      {/* The Header component is rendered on every page. */}
      <Header />
      {/* The Routes component defines the routes for the application. */}
      <Routes>
        {/* Each Route component defines a single route. */}
        {/* The path prop specifies the path for the route. */}
        {/* The element prop specifies the component to render for the route. */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/books" element={<BookList />} />
        <Route path="/books/:id" element={<BookDetail />} />
        <Route path="/search" element={<Search />} />
      </Routes>
    </Router>
  );
}

export default App;
