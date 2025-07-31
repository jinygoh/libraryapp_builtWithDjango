// This file defines the BookAuthor model for the application.
// The BookAuthor model is an intermediate model that links the Book and Author models.
// It represents the 'books_authors' table in the database.

const { Model, DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  // The BookAuthor class extends the Sequelize Model class.
  class BookAuthor extends Model {}

  // The init method initializes the model with its attributes and options.
  BookAuthor.init({
    // The id attribute is the primary key for the table.
    // It is an auto-incrementing integer.
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
    },
    // The bookId attribute is a foreign key that references the 'books' table.
    bookId: {
      type: DataTypes.INTEGER,
      references: {
        model: 'Book',
        key: 'id',
      },
    },
    // The authorId attribute is a foreign key that references the 'authors' table.
    authorId: {
      type: DataTypes.INTEGER,
      references: {
        model: 'Author',
        key: 'id',
      },
    },
  }, {
    // The sequelize instance is passed to the model.
    sequelize,
    // The model name is set to 'BookAuthor'.
    modelName: 'BookAuthor',
    // The table name is explicitly set to 'books_authors'.
    tableName: 'books_authors',
    // Timestamps (createdAt and updatedAt) are enabled by default.
    timestamps: true,
  });

  return BookAuthor;
};
