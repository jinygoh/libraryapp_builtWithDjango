// This file is responsible for creating and configuring the Sequelize instance.
// Sequelize is a promise-based Node.js ORM for Postgres, MySQL, MariaDB, SQLite and Microsoft SQL Server.
// It features solid transaction support, relations, eager and lazy loading, read replication and more.

// Import the Sequelize library.
const { Sequelize } = require('sequelize');

// Import the database configuration from the config.json file.
// The `NODE_ENV` environment variable is used to determine which configuration to use (development, test, or production).
// If `NODE_ENV` is not set, it defaults to 'development'.
const env = process.env.NODE_ENV || 'development';
const config = require('./config.json')[env];

// Create a new Sequelize instance.
// The instance is configured with the database credentials from the config.json file.
const sequelize = new Sequelize(config.database, config.username, config.password, {
  host: config.host,
  dialect: config.dialect,
});

// Export the Sequelize instance to be used in other parts of the application.
module.exports = sequelize;
