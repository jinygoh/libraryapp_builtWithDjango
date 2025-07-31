// This file defines the Loan model for the application.
// The Loan model represents the 'loans' table in the database.
// It includes fields for borrow date, due date, return date, and the status of the loan.

const { Model, DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  // The Loan class extends the Sequelize Model class.
  class Loan extends Model {
    // This method is used to define the associations between the Loan model and other models.
    static associate(models) {
      // A loan belongs to a user.
      Loan.belongsTo(models.User, { foreignKey: 'userId' });
      // A loan belongs to a book.
      Loan.belongsTo(models.Book, { foreignKey: 'bookId' });
      // A loan can have one fine.
      Loan.hasOne(models.Fine, { foreignKey: 'loanId' });
    }
  }

  // The init method initializes the model with its attributes and options.
  Loan.init({
    // The id attribute is the primary key for the table.
    // It is an auto-incrementing integer.
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
    },
    // The borrow_date attribute is a date that defaults to the current date and time.
    borrow_date: {
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW,
    },
    // The due_date attribute is a date.
    due_date: {
      type: DataTypes.DATE,
      allowNull: false,
    },
    // The return_date attribute is a date that can be null.
    return_date: {
      type: DataTypes.DATE,
      allowNull: true,
    },
    // The status attribute is an enum that can have one of three values: 'borrowed', 'returned', or 'overdue'.
    // It defaults to 'borrowed'.
    status: {
      type: DataTypes.ENUM('borrowed', 'returned', 'overdue'),
      defaultValue: 'borrowed',
    },
  }, {
    // The sequelize instance is passed to the model.
    sequelize,
    // The model name is set to 'Loan'.
    modelName: 'Loan',
    // The table name is explicitly set to 'loans'.
    tableName: 'loans',
    // Timestamps (createdAt and updatedAt) are enabled by default.
    timestamps: true,
  });

  return Loan;
};
