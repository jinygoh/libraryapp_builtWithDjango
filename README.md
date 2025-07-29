# Silent Library

Silent Library is a web-based application for managing a library's collection of books and their members. It provides a simple and intuitive interface for both library staff and members to interact with the library's resources.

## Features

*   **User Authentication**: Members can register for an account, log in, and manage their profile.
*   **Book Catalog**: Members can search for books by title, author, or genre.
*   **Borrowing and Returning**: Members can borrow and return books.
*   **Reviews and Ratings**: Members can write reviews and rate books they have borrowed.
*   **Staff Dashboard**: Staff members have access to a dashboard where they can manage books, users, and loans.
*   **Overdue Notifications**: Staff members can send bulk email notifications to members with overdue books.

## Technologies Used

*   **Backend**: Django, Python
*   **Frontend**: HTML, CSS, Bootstrap
*   **Database**: MySQL

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

*   Python 3.8 or higher
*   pip
*   MySQL

### Installation

1.  **Clone the repository**:
    ```sh
    git clone https://github.com/your_username/silent-library.git
    ```
2.  **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```
4.  **Set up the database**:
    *   Create a MySQL database for the project.
    *   Create a `.env` file in the `silent_library` directory and add the following environment variables:
        ```
        DJANGO_SECRET_KEY=your_secret_key
        DB_NAME=your_db_name
        DB_USER=your_db_user
        DB_PASSWORD=your_db_password
        EMAIL_HOST_USER=your_email
        EMAIL_HOST_PASSWORD=your_email_password
        ```
5.  **Run the migrations**:
    ```sh
    python silent_library/manage.py migrate
    ```
6.  **Create a superuser**:
    ```sh
    python silent_library/manage.py createsuperuser
    ```
7.  **Run the development server**:
    ```sh
    python silent_library/manage.py runserver
    ```

## Usage

*   Access the application at `http://127.0.0.1:8000/`.
*   Access the admin panel at `http://127.0.0.1:8000/admin/`.

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.
