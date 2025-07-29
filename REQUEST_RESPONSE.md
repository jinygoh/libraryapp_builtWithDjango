# Request and Response Flow

This document explains the request and response flow for each endpoint in the Silent Library project.

## User Authentication

### `/register/`

*   **Request**: `GET` or `POST`
    *   `GET`: Displays the user registration form.
    *   `POST`: Submits the registration form with user data (username, email, password, etc.).
*   **View**: `library.views.register`
*   **Logic**:
    1.  If the request is `GET`, it renders the `library/register.html` template with an empty registration form.
    2.  If the request is `POST`, it validates the form data.
    3.  If the form is valid, it creates a new user, sends a confirmation email, and redirects to the `/register/complete/` page.
    4.  If the form is invalid, it re-renders the `library/register.html` template with the form and validation errors.
*   **Response**:
    *   `GET`: Renders the registration page.
    *   `POST` (success): Redirects to the registration complete page.
    *   `POST` (failure): Renders the registration page with errors.

### `/login/`

*   **Request**: `GET` or `POST`
    *   `GET`: Displays the user login form.
    *   `POST`: Submits the login form with user credentials (username and password).
*   **View**: `library.views.login_view`
*   **Logic**:
    1.  If the request is `GET`, it renders the `library/login.html` template with an empty login form.
    2.  If the request is `POST`, it authenticates the user.
    3.  If authentication is successful, it logs the user in and redirects to the dashboard (`/dashboard/`).
    4.  If authentication fails, it re-renders the `library/login.html` template with an error message.
*   **Response**:
    *   `GET`: Renders the login page.
    *   `POST` (success): Redirects to the dashboard.
    *   `POST` (failure): Renders the login page with an error message.

### `/logout/`

*   **Request**: `GET`
*   **View**: `library.views.logout_view`
*   **Logic**: Logs the user out and redirects to the home page (`/`).
*   **Response**: Redirects to the home page.

## Core Features

### `/` (Home)

*   **Request**: `GET`
*   **View**: `library.views.home`
*   **Logic**: Renders the `library/home.html` template.
*   **Response**: Renders the home page.

### `/dashboard/`

*   **Request**: `GET`
*   **View**: `library.views.dashboard`
*   **Logic**:
    1.  Requires the user to be logged in.
    2.  Retrieves the user's loans and reviews from the database.
    3.  Renders the `library/dashboard.html` template with the user's data.
*   **Response**: Renders the user dashboard.

### `/profile/`

*   **Request**: `GET` or `POST`
    *   `GET`: Displays the user's profile information and forms for editing it.
    *   `POST`: Submits one of the forms to update the user's profile.
*   **View**: `library.views.profile`
*   **Logic**:
    1.  Requires the user to be logged in.
    2.  Handles multiple forms for updating different parts of the user's profile (personal info, username/email, password).
    3.  If a form is submitted and valid, it updates the user's data and redirects back to the profile page.
*   **Response**: Renders the profile page with updated information or validation errors.

### `/search/`

*   **Request**: `GET`
*   **View**: `library.views.search_books`
*   **Logic**:
    1.  Retrieves the search query from the request's GET parameters.
    2.  Filters the books in the database based on the query (title, author, genre).
    3.  Renders the `library/search.html` template with the search results.
*   **Response**: Renders the search results page.

### `/book/<int:book_id>/`

*   **Request**: `GET` or `POST`
    *   `GET`: Displays the details of a specific book, including its reviews.
    *   `POST`: Submits a new review for the book.
*   **View**: `library.views.book_detail`
*   **Logic**:
    1.  Retrieves the book with the specified ID from the database.
    2.  If the request is `POST`, it validates the review form and saves the new review.
    3.  Renders the `library/book_detail.html` template with the book's details and reviews.
*   **Response**: Renders the book detail page.

## Staff Features

### `/staff/`

*   **Request**: `GET`
*   **View**: `library.views.admin_dashboard`
*   **Logic**:
    1.  Requires the user to be a staff member.
    2.  Retrieves data about active loans, overdue books, and fines.
    3.  Renders the `library/staff_dashboard.html` template with the administrative data.
*   **Response**: Renders the admin dashboard.

### `/staff/books/`

*   **Request**: `GET`
*   **View**: `library.views.admin_books`
*   **Logic**:
    1.  Requires the user to be a staff member.
    2.  Retrieves a list of all books from the database.
    3.  Renders the `library/staff_books.html` template with the list of books.
*   **Response**: Renders the book management page.

### `/staff/users/`

*   **Request**: `GET`
*   **View**: `library.views.admin_users`
*   **Logic**:
    1.  Requires the user to be a staff member.
    2.  Retrieves a list of all users from the database.
    3.  Renders the `library/staff_users.html` template with the list of users.
*   **Response**: Renders the user management page.
