// This file defines the Fine model for the application.
// The Fine model represents the 'fines' table in the database.
// It includes fields for the fine amount, payment status, and other fine-related information.

const { Model, DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  // The Fine class extends the Sequelize Model class.
  class Fine extends Model {
    // This method is used to define the associations between the Fine model and other models.
    static associate(models) {
      // A fine belongs to a loan.
      Fine.belongsTo(models.Loan, { foreignKey: 'loanId' });
    }
  }

  // The init method initializes the model with its attributes and options.
  Fine.init({
    // The id attribute is the primary key for the table.
    // It is an auto-incrementing integer.
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
    },
    // The fine_amount attribute is a decimal number.
    fine_amount: {
      type: DataTypes.DECIMAL(10, 2),
      allowNull: false,
    },
    // The payment_status attribute is an enum that can have one of three values: 'pending', 'paid', or 'waived'.
    // It defaults to 'pending'.
    payment_status: {
      type: DataTypes.ENUM('pending', 'paid', 'waived'),
      defaultValue: 'pending',
    },
    // The fine_date attribute is a date that defaults to the current date and time.
    fine_date: {
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW,
    },
    // The payment_date attribute is a date that can be null.
    payment_date: {
      type: DataTypes.DATE,
      allowNull: true,
    },
  }, {
    // The sequelize instance is passed to the model.
    sequelize,
    // The model name is set to 'Fine'.
    modelName: 'Fine',
    // The table name is explicitly set to 'fines'.
    tableName: 'fines',
    // Timestamps (createdAt and updatedAt) are enabled by default.
    timestamps: true,
  });

  return Fine;
};
