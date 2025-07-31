// This file defines the Book model for the application.
// The Book model represents the 'books' table in the database.
// It includes fields for title, ISBN, and other book-related information.

const { Model, DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  // The Book class extends the Sequelize Model class.
  class Book extends Model {
    // This method is used to define the associations between the Book model and other models.
    static associate(models) {
      // A book can have many authors.
      // The 'through' option specifies the intermediate model that links the Book and Author models.
      Book.belongsToMany(models.Author, { through: 'BookAuthor', foreignKey: 'bookId' });
      // A book can have many genres.
      // The 'through' option specifies the intermediate model that links the Book and Genre models.
      Book.belongsToMany(models.Genre, { through: 'BookGenre', foreignKey: 'bookId' });
      // A book can have many loans.
      Book.hasMany(models.Loan, { foreignKey: 'bookId' });
      // A book can have many reviews.
      Book.hasMany(models.Review, { foreignKey: 'bookId' });
    }
  }

  // The init method initializes the model with its attributes and options.
  Book.init({
    // The id attribute is the primary key for the table.
    // It is an auto-incrementing integer.
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
    },
    // The title attribute is a string.
    title: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    // The isbn attribute is a string that must be unique.
    isbn: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true,
    },
    // The total_copies attribute is an integer that defaults to 1.
    total_copies: {
      type: DataTypes.INTEGER,
      defaultValue: 1,
    },
    // The available_copies attribute is an integer that defaults to 1.
    available_copies: {
      type: DataTypes.INTEGER,
      defaultValue: 1,
    },
    // The image attribute is a string that can be null.
    // It is used to store the path to the book's image.
    image: {
      type: DataTypes.STRING,
      allowNull: true,
    },
  }, {
    // The sequelize instance is passed to the model.
    sequelize,
    // The model name is set to 'Book'.
    modelName: 'Book',
    // The table name is explicitly set to 'books'.
    tableName: 'books',
    // Timestamps (createdAt and updatedAt) are enabled by default.
    timestamps: true,
    // This constraint ensures that the number of available copies is always less than or equal to the total number of copies.
    validate: {
        availableCopiesLteTotalCopies() {
            if (this.available_copies > this.total_copies) {
                throw new Error('Available copies cannot be greater than total copies.');
            }
        }
    }
  });

  return Book;
};
