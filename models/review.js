// This file defines the Review model for the application.
// The Review model represents the 'reviews' table in the database.
// It includes fields for the review rating, text, and the user and book associated with the review.

const { Model, DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  // The Review class extends the Sequelize Model class.
  class Review extends Model {
    // This method is used to define the associations between the Review model and other models.
    static associate(models) {
      // A review belongs to a user.
      Review.belongsTo(models.User, { foreignKey: 'userId' });
      // A review belongs to a book.
      Review.belongsTo(models.Book, { foreignKey: 'bookId' });
    }
  }

  // The init method initializes the model with its attributes and options.
  Review.init({
    // The id attribute is the primary key for the table.
    // It is an auto-incrementing integer.
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
    },
    // The rating attribute is an integer that must be between 1 and 5.
    rating: {
      type: DataTypes.INTEGER,
      allowNull: false,
      validate: {
        min: 1,
        max: 5,
      },
    },
    // The review_text attribute is a text field.
    review_text: {
      type: DataTypes.TEXT,
      allowNull: false,
    },
    // The review_date attribute is a date that defaults to the current date and time.
    review_date: {
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW,
    },
  }, {
    // The sequelize instance is passed to the model.
    sequelize,
    // The model name is set to 'Review'.
    modelName: 'Review',
    // The table name is explicitly set to 'reviews'.
    tableName: 'reviews',
    // Timestamps (createdAt and updatedAt) are enabled by default.
    timestamps: true,
  });

  return Review;
};
