// This file defines the Author model for the application.
// The Author model represents the 'authors' table in the database.
// It includes fields for the author's first and last name.

const { Model, DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  // The Author class extends the Sequelize Model class.
  class Author extends Model {
    // This method is used to define the associations between the Author model and other models.
    static associate(models) {
      // An author can have many books.
      // The 'through' option specifies the intermediate model that links the Author and Book models.
      Author.belongsToMany(models.Book, { through: 'BookAuthor', foreignKey: 'authorId' });
    }
  }

  // The init method initializes the model with its attributes and options.
  Author.init({
    // The id attribute is the primary key for the table.
    // It is an auto-incrementing integer.
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
    },
    // The first_name attribute is a string.
    first_name: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    // The last_name attribute is a string.
    last_name: {
      type: DataTypes.STRING,
      allowNull: false,
    },
  }, {
    // The sequelize instance is passed to the model.
    sequelize,
    // The model name is set to 'Author'.
    modelName: 'Author',
    // The table name is explicitly set to 'authors'.
    tableName: 'authors',
    // Timestamps (createdAt and updatedAt) are enabled by default.
    timestamps: true,
  });

  return Author;
};
