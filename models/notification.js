// This file defines the Notification model for the application.
// The Notification model represents the 'notifications' table in the database.
// It includes fields for the notification text and the user who should receive the notification.

const { Model, DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  // The Notification class extends the Sequelize Model class.
  class Notification extends Model {
    // This method is used to define the associations between the Notification model and other models.
    static associate(models) {
      // A notification belongs to a user.
      Notification.belongsTo(models.User, { foreignKey: 'userId' });
    }
  }

  // The init method initializes the model with its attributes and options.
  Notification.init({
    // The id attribute is the primary key for the table.
    // It is an auto-incrementing integer.
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
    },
    // The timestamp attribute is a date that defaults to the current date and time.
    timestamp: {
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW,
    },
    // The notification_text attribute is a string.
    notification_text: {
      type: DataTypes.STRING(512),
      allowNull: false,
    },
  }, {
    // The sequelize instance is passed to the model.
    sequelize,
    // The model name is set to 'Notification'.
    modelName: 'Notification',
    // The table name is explicitly set to 'notifications'.
    tableName: 'notifications',
    // Timestamps (createdAt and updatedAt) are enabled by default.
    timestamps: true,
  });

  return Notification;
};
