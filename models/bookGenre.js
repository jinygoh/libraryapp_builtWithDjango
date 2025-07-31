// This file defines the BookGenre model for the application.
// The BookGenre model is an intermediate model that links the Book and Genre models.
// It represents the 'books_genres' table in the database.

const { Model, DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  // The BookGenre class extends the Sequelize Model class.
  class BookGenre extends Model {}

  // The init method initializes the model with its attributes and options.
  BookGenre.init({
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
    // The genreId attribute is a foreign key that references the 'genres' table.
    genreId: {
      type: DataTypes.INTEGER,
      references: {
        model: 'Genre',
        key: 'id',
      },
    },
  }, {
    // The sequelize instance is passed to the model.
    sequelize,
    // The model name is set to 'BookGenre'.
    modelName: 'BookGenre',
    // The table name is explicitly set to 'books_genres'.
    tableName: 'books_genres',
    // Timestamps (createdAt and updatedAt) are enabled by default.
    timestamps: true,
  });

  return BookGenre;
};
