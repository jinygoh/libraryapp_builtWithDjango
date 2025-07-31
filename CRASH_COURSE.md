# React Crash Course for the Silent Library App

This document provides a crash course on how the React front end of the Silent Library application works. It will pinpoint parts of the project to show as examples.

## Project Structure

The React code is located in the `frontend` directory. Here's a breakdown of the key files and directories:

- **`frontend/public`**: This directory contains the static assets for the application, such as `index.html`.
- **`frontend/src`**: This directory contains the React source code.
  - **`frontend/src/components`**: This directory contains the React components, which are the building blocks of the UI.
  - **`frontend/src/services`**: This directory contains services that handle API calls to the Django back end.
  - **`frontend/src/App.js`**: This is the main component of the application. It sets up the routing and navigation.
  - **`frontend/src/index.js`**: This is the entry point of the application. It renders the `App` component.

## Key Concepts

### Components

Components are the fundamental building blocks of a React application. They are reusable pieces of UI that can have their own state and logic. In this project, you can find the components in the `frontend/src/components` directory. For example, the `Login.js` component handles the user login functionality.

### State

State is a JavaScript object that stores data for a component. When the state of a component changes, React re-renders the component to reflect the new state. In the `Login.js` component, the `useState` hook is used to manage the state of the username, password, loading status, and message.

### Props

Props (short for properties) are used to pass data from a parent component to a child component. This allows you to create reusable components that can be configured with different data.

### Routing

Routing is the process of navigating between different pages in an application. In this project, we use the `react-router-dom` library to handle routing. The routes are defined in the `App.js` file.

### Services

Services are used to encapsulate the logic for making API calls to the back end. This helps to keep the components clean and focused on the UI. In this project, you can find the services in the `frontend/src/services` directory. For example, the `AuthService.js` handles API calls for user authentication.

## How the App Works

1.  **User Authentication**: When a user visits the application, they are presented with a login page. They can either log in with their existing credentials or register for a new account. The `Login.js` and `Register.js` components handle these actions, respectively. They use the `AuthService.js` to make API calls to the Django back end.

2.  **Dashboard**: Once a user is logged in, they are redirected to the dashboard. The `Dashboard.js` component fetches the user's borrowed books and reviews from the back end and displays them.

3.  **Book Search**: Users can search for books using the search bar on the home page. The `Search.js` component handles the search functionality. It uses the `BookService.js` to make API calls to the back end.

4.  **Book Detail Page**: When a user clicks on a book from the search results, they are taken to the book detail page. The `Book.js` component fetches the book details and reviews from the back end and displays them.

## Conclusion

This crash course provides a high-level overview of how the React front end of the Silent Library application works. To learn more, you can explore the code in the `frontend` directory and refer to the official React documentation.
