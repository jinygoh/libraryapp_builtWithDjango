# Express.js Crash Course

This document provides a crash course on Express.js, using the code from this project as examples.

## 1. What is Express.js?

Express.js is a minimal and flexible Node.js web application framework that provides a robust set of features for web and mobile applications. It is the most popular web framework for Node.js.

## 2. Core Concepts

### 2.1. The Server

The entry point of our application is `server.js`. This file is responsible for creating the Express server, setting up middleware, and defining the routes.

```javascript
// server.js

// Import necessary libraries
const express = require('express');

// Create an Express application
const app = express();

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
```

In this snippet, we import the `express` library and create an instance of the application. The `app.listen()` function starts the server and makes it listen for incoming requests on a specified port.

### 2.2. Routing

Routing refers to how an application's endpoints (URIs) respond to client requests. You define routing using methods of the Express `app` object that correspond to HTTP methods; for example, `app.get()` to handle GET requests and `app.post()` for POST requests.

In our project, we have organized our routes into separate files in the `routes` directory. For example, `routes/auth.js` handles authentication-related routes.

```javascript
// routes/auth.js

const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');

// This route renders the login page.
router.get('/login', authController.getLogin);

// This route handles the login form submission.
router.post('/login', authController.postLogin);

module.exports = router;
```

We use `express.Router()` to create a modular, mountable route handler. This allows us to group our routes and keep our code organized.

### 2.3. Middleware

Middleware functions are functions that have access to the request object (`req`), the response object (`res`), and the `next` function in the application's request-response cycle. The `next` function is a function in the Express router which, when invoked, executes the middleware succeeding the current middleware.

Middleware can:
- Execute any code.
- Make changes to the request and the response objects.
- End the request-response cycle.
- Call the next middleware in the stack.

In our project, we use middleware for various purposes, such as parsing request bodies, serving static files, and handling sessions.

```javascript
// server.js

// The 'express.json' and 'express.urlencoded' middleware are used to parse incoming requests.
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// The 'express.static' middleware is used to serve static files.
app.use(express.static(path.join(__dirname, 'public')));
```

We also have custom middleware for authentication and authorization in `middleware/auth.js`.

```javascript
// middleware/auth.js

exports.isAuthenticated = (req, res, next) => {
  if (req.session.user) {
    return next();
  }
  res.redirect('/login');
};
```

### 2.4. Templating

Templating engines allow you to use static template files in your application. At runtime, the templating engine replaces variables in a template file with actual values, and transforms the template into an HTML file sent to the client.

We are using EJS (Embedded JavaScript) as our templating engine. We configure it in `server.js`.

```javascript
// server.js

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
```

We can then render our EJS templates from our controllers.

```javascript
// controllers/indexController.js

exports.getHome = (req, res, next) => {
  res.render('home');
};
```

The `res.render()` function renders a view and sends the rendered HTML string to the client.

### 2.5. Working with a Database

We are using Sequelize, a promise-based Node.js ORM, to interact with our PostgreSQL database. We define our models in the `models` directory. For example, `models/user.js` defines the `User` model.

```javascript
// models/user.js

const { Model, DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  class User extends Model {}
  User.init({
    username: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true,
    },
    // ... other fields
  }, {
    sequelize,
    modelName: 'User',
  });
  return User;
};
```

We can then use these models in our controllers to perform CRUD operations.

```javascript
// controllers/authController.js

const { User } = require('../models');

exports.postRegister = async (req, res, next) => {
  const { username, password } = req.body;
  try {
    const user = await User.create({ username, password });
    res.redirect('/login');
  } catch (error) {
    next(error);
  }
};
```

This crash course provides a brief overview of the key concepts in Express.js. For more detailed information, please refer to the official Express.js documentation.
