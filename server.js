// This is the main server file for the Express.js application.
// It is the entry point of the application.
// It sets up the Express app, connects to the database, configures middleware, and starts the server.

// Import necessary libraries
const express = require('express');
const session = require('express-session');
const flash = require('connect-flash');
const cookieParser = require('cookie-parser');
const path = require('path');
const ejs = require('ejs');
const expressLayouts = require('express-ejs-layouts');


// Import database connection
const sequelize = require('./config/database');

// Import routes
const indexRoutes = require('./routes/index');
const authRoutes = require('./routes/auth');
const userRoutes = require('./routes/users');
const bookRoutes = require('./routes/books');
const staffRoutes = require('./routes/staff');

// Create an Express application
const app = express();

// Set up the view engine
// The 'express-ejs-layouts' middleware is used to create a layout file that can be used by all the other EJS files.
app.use(expressLayouts);
app.set('layout', './layouts/main'); // not using this for now
// The 'view engine' is set to 'ejs'.
// The 'views' directory is set to the 'views' directory in the project root.
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));


// Set up middleware
// The 'express.json' and 'express.urlencoded' middleware are used to parse incoming requests with JSON and URL-encoded payloads.
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
// The 'cookie-parser' middleware is used to parse cookies from the request.
app.use(cookieParser());
// The 'express.static' middleware is used to serve static files like images, CSS, and JavaScript.
app.use(express.static(path.join(__dirname, 'public')));
// The 'express-session' middleware is used to create and manage user sessions.
app.use(session({
    secret: 'secret', // This should be a long, random string in a real application.
    resave: false,
    saveUninitialized: false,
}));
// The 'connect-flash' middleware is used to display flash messages to the user.
app.use(flash());

// Set up a global middleware to make flash messages available in all templates.
app.use((req, res, next) => {
    res.locals.success_msg = req.flash('success_msg');
    res.locals.error_msg = req.flash('error_msg');
    res.locals.error = req.flash('error');
    next();
});

// Set up routes
// The routes are mounted on the application.
app.use('/', indexRoutes);
app.use('/', authRoutes);
app.use('/', userRoutes);
app.use('/', bookRoutes);
app.use('/staff', staffRoutes);


// Set up a 404 error handler.
// This middleware is called if no other route matches the request.
app.use((req, res, next) => {
    res.status(404).send('Page not found');
});

// Set up a general error handler.
// This middleware is called if an error occurs in any of the routes.
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Something broke!');
});


// Start the server
// The server listens on port 3000.
// Before starting the server, it syncs the database schema.
const PORT = process.env.PORT || 3000;
sequelize.sync().then(() => {
    app.listen(PORT, () => {
        console.log(`Server is running on port ${PORT}`);
    });
});
