# Request and Response Cycle

This document explains the request and response cycle for each of the main functions in the application.

## User Registration

1.  **React Frontend (`Register.js`):**
    *   The user fills out the registration form and clicks the "Register" button.
    *   The `handleSubmit` function is called, which makes a POST request to the `/register` endpoint of the backend API.
    *   The request body contains the user's registration information (username, password, email, first name, last name).

2.  **Spring Boot Backend (`AuthenticationController.java`):**
    *   The `registerUser` method in the `AuthenticationController` handles the request.
    *   It checks if the username and email are already taken.
    *   If they are not, it creates a new `User` object and saves it to the database.
    *   It returns a success response to the frontend.

3.  **React Frontend (`Register.js`):**
    *   If the registration is successful, the user is redirected to the login page.

## User Login

1.  **React Frontend (`Login.js`):**
    *   The user fills out the login form and clicks the "Login" button.
    *   The `handleSubmit` function is called, which makes a POST request to the `/authenticate` endpoint of the backend API.
    *   The request body contains the user's credentials (username and password).

2.  **Spring Boot Backend (`AuthenticationController.java`):**
    *   The `createAuthenticationToken` method in the `AuthenticationController` handles the request.
    *   It authenticates the user using the `AuthenticationManager`.
    *   If the authentication is successful, it generates a JWT for the user.
    *   It returns the JWT in the response body.

3.  **React Frontend (`Login.js`):**
    *   If the authentication is successful, the JWT is stored in local storage.
    *   The user is redirected to the dashboard page.

## Get All Books

1.  **React Frontend (`BookList.js`):**
    *   The `BookList` component mounts, and the `useEffect` hook is called.
    *   The `fetchBooks` function is called, which makes a GET request to the `/api/books` endpoint of the backend API.

2.  **Spring Boot Backend (`BookController.java`):**
    *   The `getAllBooks` method in the `BookController` handles the request.
    *   It fetches all books from the database using the `BookRepository`.
    *   It returns a list of all books in the response body.

3.  **React Frontend (`BookList.js`):**
    *   The `books` state variable is updated with the list of books from the response.
    *   The component re-renders to display the list of books.

## Borrow a Book

1.  **React Frontend (to be implemented):**
    *   The user clicks a "Borrow" button for a specific book.
    *   A function is called that makes a POST request to the `/api/loans/borrow/{bookId}` endpoint of the backend API.

2.  **Spring Boot Backend (`LoanController.java`):**
    *   The `borrowBook` method in the `LoanController` handles the request.
    *   It gets the currently authenticated user.
    *   It checks if the user is blocked and if the book is available.
    *   If everything is okay, it creates a new `Loan` object and saves it to the database.
    *   It decrements the number of available copies of the book.
    *   It returns a success response.

3.  **React Frontend (to be implemented):**
    *   The UI is updated to reflect that the book has been borrowed.
