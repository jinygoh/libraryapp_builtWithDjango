// This file defines the User model for the application.
// The User model represents the 'users' table in the database.
// It includes fields for username, password, email, and other user-related information.
// It also includes a hook to hash the user's password before saving it to the database.

const { Model, DataTypes } = require('sequelize');
const bcrypt = require('bcrypt');

module.exports = (sequelize) => {
  // The User class extends the Sequelize Model class.
  class User extends Model {
    // This method is used to define the associations between the User model and other models.
    static associate(models) {
      // A user can have many loans.
      User.hasMany(models.Loan, { foreignKey: 'userId' });
      // A user can have many reviews.
      User.hasMany(models.Review, { foreignKey: 'userId' });
      // A user can have many notifications.
      User.hasMany(models.Notification, { foreignKey: 'userId' });
    }

    // This is an instance method that can be used to check if a given password is valid.
    // It compares the given password with the hashed password stored in the database.
    validPassword(password) {
      return bcrypt.compareSync(password, this.password);
    }
  }

  // The init method initializes the model with its attributes and options.
  User.init({
    // The id attribute is the primary key for the table.
    // It is an auto-incrementing integer.
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
    },
    // The username attribute is a string that must be unique.
    username: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true,
    },
    // The password attribute is a string that cannot be null.
    password: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    // The email attribute is a string that must be unique and a valid email address.
    email: {
      type: DataTypes.STRING,
      allowNull:false,
      unique: true,
      validate: {
        isEmail: true,
      },
    },
    // The first_name attribute is a string.
    first_name: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    // The last_name attribute is a string.
    last_name: {
        type: DataTypes.STRING,
        allowNull: true,
    },
    // The date_of_birth attribute is a date.
    date_of_birth: {
      type: DataTypes.DATE,
      allowNull: true,
    },
    // The is_blocked attribute is a boolean that defaults to false.
    // It is used to block a user from accessing the library.
    is_blocked: {
      type: DataTypes.BOOLEAN,
      defaultValue: false,
    },
    // The is_staff attribute is a boolean that defaults to false.
    // It is used to identify staff members who have access to the admin dashboard.
    is_staff: {
        type: DataTypes.BOOLEAN,
        defaultValue: false,
    },
  }, {
    // The sequelize instance is passed to the model.
    sequelize,
    // The model name is set to 'User'.
    modelName: 'User',
    // The table name is explicitly set to 'users'.
    tableName: 'users',
    // Timestamps (createdAt and updatedAt) are enabled by default.
    timestamps: true,
    // This hook is executed before a new user is created.
    // It hashes the user's password using bcrypt.
    hooks: {
      beforeCreate: async (user) => {
        if (user.password) {
          const salt = await bcrypt.genSalt(10);
          user.password = await bcrypt.hash(user.password, salt);
        }
      },
      // This hook is executed before an existing user is updated.
      // It hashes the user's password if it has been changed.
      beforeUpdate: async (user) => {
        if (user.changed('password')) {
          const salt = await bcrypt.genSalt(10);
          user.password = await bcrypt.hash(user.password, salt);
        }
      },
    },
  });

  return User;
};
