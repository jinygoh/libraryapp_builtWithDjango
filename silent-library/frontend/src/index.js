// This is the entry point for the React application.
// It renders the main App component to the DOM.

import React from 'react';
// Import the ReactDOM library for rendering React components to the DOM.
import ReactDOM from 'react-dom/client';
// Import the main stylesheet for the application.
import './index.css';
// Import the main App component.
import App from './App';
// Import the reportWebVitals function for measuring web performance.
import reportWebVitals from './reportWebVitals';

// Get the root element from the DOM.
const root = ReactDOM.createRoot(document.getElementById('root'));
// Render the App component to the root element.
root.render(
  // The StrictMode component highlights potential problems in an application.
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
