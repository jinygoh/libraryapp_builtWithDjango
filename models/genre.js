// This file defines the Genre model for the application.
// The Genre model represents the 'genres' table in the database.
// It includes a field for the genre name.

const { Model, DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  // The Genre class extends the Sequelize Model class.
  class Genre extends Model {
    // This method is used to define the associations between the Genre model and other models.
    static associate(models) {
      // A genre can have many books.
      // The 'through' option specifies the intermediate model that links the Genre and Book models.
      Genre.belongsToMany(models.Book, { through: 'BookGenre', foreignKey: 'genreId' });
    }
  }

  // The init method initializes the model with its attributes and options.
  Genre.init({
    // The id attribute is the primary key for the table.
    // It is an auto-incrementing integer.
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
    },
    // The genre attribute is a string that must be unique.
    genre: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true,
    },
  }, {
    // The sequelize instance is passed to the model.
    sequelize,
    // The model name is set to 'Genre'.
    modelName: 'Genre',
    // The table name is explicitly set to 'genres'.
    tableName: 'genres',
    // Timestamps (createdAt and updatedAt) are enabled by default.
    timestamps: true,
  });

  return Genre;
};
