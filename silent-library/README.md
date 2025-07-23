# Silent Library

This project is a web application for a library management system, built with Spring Boot for the backend and React for the frontend.

## Project Structure

The project is divided into two main parts:

-   `backend`: A Spring Boot application that provides the REST APIs for the application.
-   `frontend`: A React application that provides the user interface.

### Backend

The backend is a standard Maven project with the following structure:

-   `src/main/java/com/example/silentlibrary`: Contains the main source code for the application.
    -   `config`: Contains the Spring Security configuration.
    -   `controllers`: Contains the REST controllers that handle the API requests.
    -   `models`: Contains the JPA entities and DTOs.
    -   `repositories`: Contains the Spring Data JPA repositories for database operations.
    -   `services`: Contains the business logic for the application.
    -   `utils`: Contains utility classes, such as the `JwtUtil` for handling JWTs.
-   `src/main/resources`: Contains the application configuration files.
-   `pom.xml`: The Maven project configuration file.

### Frontend

The frontend is a standard React application created with `create-react-app`.

-   `public`: Contains the public assets for the application.
-   `src`: Contains the main source code for the application.
    -   `components`: Contains the React components.
    -   `axios.js`: A pre-configured `axios` instance for making API requests.
    -   `App.js`: The main application component.
    -   `index.js`: The entry point for the application.
-   `package.json`: The Node.js project configuration file.

## How to Run the Application

### Backend

To run the backend, you will need to have Java and Maven installed.

1.  Navigate to the `silent-library` directory.
2.  Run the following command:

    ```bash
    mvn spring-boot:run
    ```

The backend will start on port 8080.

### Frontend

To run the frontend, you will need to have Node.js and npm installed.

1.  Navigate to the `silent-library/frontend` directory.
2.  Run the following command to install the dependencies:

    ```bash
    npm install
    ```

3.  Run the following command to start the development server:

    ```bash
    npm start
    ```

The frontend will start on port 3000.
