/**
 * This component handles the user logout process.
 */
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthService from '../services/AuthService';

const Logout = () => {
  // Hook for navigation
  const navigate = useNavigate();

  // useEffect hook to run the logout process when the component mounts
  useEffect(() => {
    // Call the logout method from the AuthService
    AuthService.logout();
    // Navigate to the login page and reload the page
    navigate('/login');
    window.location.reload();
  }, [navigate]);

  return <div>Logging out...</div>;
};

export default Logout;
