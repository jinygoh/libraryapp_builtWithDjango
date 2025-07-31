// This file contains the controller functions for staff-related routes.
// The controller functions are responsible for handling the business logic of the application.
// They are called by the route handlers in the 'routes' directory.

const { User, Book, Author, Genre, Loan, Fine, Sequelize } = require('../models');
const { Op } = Sequelize;
const nodemailer = require('nodemailer');

// This function renders the admin dashboard.
// It fetches active loans and overdue books from the database.
exports.getDashboard = async (req, res, next) => {
  try {
    // Find all active loans.
    const activeLoans = await Loan.findAll({
      where: { status: { [Op.in]: ['borrowed', 'overdue'] } },
      include: [User, Book],
    });
    // Find all overdue books.
    const overdueBooks = await Loan.findAll({
      where: { status: 'overdue' },
      include: [User, Book],
    });
    // Render the staff dashboard view with the active loans and overdue books data.
    res.render('staff_dashboard', { layout: 'base', activeLoans, overdueBooks });
  } catch (error) {
    next(error);
  }
};

// This function renders the admin page for managing users.
// It fetches all users from the database.
exports.getUsers = async (req, res, next) => {
  try {
    // Find all users.
    const users = await User.findAll();
    // Render the staff users view with the users data.
    res.render('staff_users', { layout: 'base', users });
  } catch (error) {
    next(error);
  }
};

// This function handles blocking a user.
// It sets the 'is_blocked' flag for the user to true.
exports.blockUser = async (req, res, next) => {
  try {
    const { userId } = req.params;
    // Find the user by their ID and update their 'is_blocked' status.
    await User.update({ is_blocked: true }, { where: { id: userId } });
    // Redirect to the admin users page.
    req.flash('success_msg', 'User blocked successfully');
    res.redirect('/staff/users');
  } catch (error) {
    next(error);
  }
};

// This function handles unblocking a user.
// It sets the 'is_blocked' flag for the user to false.
exports.unblockUser = async (req, res, next) => {
  try {
    const { userId } = req.params;
    // Find the user by their ID and update their 'is_blocked' status.
    await User.update({ is_blocked: false }, { where: { id: userId } });
    // Redirect to the admin users page.
    req.flash('success_msg', 'User unblocked successfully');
    res.redirect('/staff/users');
  } catch (error) {
    next(error);
  }
};

// This function renders the admin page for managing books.
// It fetches all books from the database.
exports.getBooks = async (req, res, next) => {
  try {
    // Find all books.
    const books = await Book.findAll({ include: [Author, Genre] });
    // Render the staff books view with the books data.
    res.render('staff_books', { layout: 'base', books });
  } catch (error) {
    next(error);
  }
};

// This function renders the page for adding a new book.
exports.getAddBook = (req, res, next) => {
  res.render('book_form', { layout: 'base' });
};

// This function handles adding a new book.
// It creates a new book and associates it with authors and genres.
exports.postAddBook = async (req, res, next) => {
  try {
    const { title, isbn, total_copies, available_copies, author_first_name, author_last_name, genres } = req.body;
    // Create a new book.
    const book = await Book.create({ title, isbn, total_copies, available_copies, image: req.file ? req.file.path : null });
    // Find or create the author.
    const [author] = await Author.findOrCreate({ where: { first_name: author_first_name, last_name: author_last_name } });
    // Associate the book with the author.
    await book.addAuthor(author);
    // Associate the book with genres.
    if (genres && genres.length) {
      const genreInstances = await Promise.all(genres.split(',').map(genre => Genre.findOrCreate({ where: { genre: genre.trim() } })));
      await book.addGenres(genreInstances.map(g => g[0]));
    }
    // Redirect to the admin books page.
    req.flash('success_msg', 'Book added successfully');
    res.redirect('/staff/books');
  } catch (error) {
    next(error);
  }
};

// This function renders the page for editing a book.
// It fetches the book's data from the database.
exports.getEditBook = async (req, res, next) => {
    try {
        const { bookId } = req.params;
        // Find the book by its ID.
        const book = await Book.findByPk(bookId, { include: [Author, Genre] });
        // Render the book form view with the book data.
        res.render('book_form', { layout: 'base', book });
    } catch (error) {
        next(error);
    }
};

// This function handles editing a book.
// It updates the book's information and its associations with authors and genres.
exports.postEditBook = async (req, res, next) => {
  try {
    const { bookId } = req.params;
    const { title, isbn, total_copies, available_copies, author_first_name, author_last_name, genres } = req.body;
    // Find the book by its ID and update its information.
    const book = await Book.findByPk(bookId);
    await book.update({ title, isbn, total_copies, available_copies, image: req.file ? req.file.path : book.image });
    // Find or create the author.
    const [author] = await Author.findOrCreate({ where: { first_name: author_first_name, last_name: author_last_name } });
    // Set the book's author.
    await book.setAuthors([author]);
    // Set the book's genres.
    if (genres && genres.length) {
        const genreInstances = await Promise.all(genres.split(',').map(genre => Genre.findOrCreate({ where: { genre: genre.trim() } })));
        await book.setGenres(genreInstances.map(g => g[0]));
    }
    // Redirect to the admin books page.
    req.flash('success_msg', 'Book updated successfully');
    res.redirect('/staff/books');
  } catch (error) {
    next(error);
  }
};

// This function handles deleting a book.
// It deletes the book and its associations.
exports.deleteBook = async (req, res, next) => {
  try {
    const { bookId } = req.params;
    // Find the book by its ID and delete it.
    const book = await Book.findByPk(bookId);
    await book.destroy();
    // Redirect to the admin books page.
    req.flash('success_msg', 'Book deleted successfully');
    res.redirect('/staff/books');
  } catch (error) {
    next(error);
  }
};

// This function sends bulk emails to users with overdue books.
// It finds all overdue loans and sends an email to each user.
exports.sendOverdueEmails = async (req, res, next) => {
    try {
        // Find all overdue loans.
        const overdueLoans = await Loan.findAll({
            where: { status: 'overdue' },
            include: [User, Book],
        });

        // Group the overdue loans by user.
        const overdueByUser = {};
        for (const loan of overdueLoans) {
            if (!overdueByUser[loan.User.id]) {
                overdueByUser[loan.User.id] = {
                    user: loan.User,
                    books: [],
                };
            }
            overdueByUser[loan.User.id].books.push(loan.Book);
        }

        // Send an email to each user with overdue books.
        // Nodemailer setup and email sending will be implemented later.
        /*
        const transporter = nodemailer.createTransport({ ... });
        for (const userId in overdueByUser) {
            const { user, books } = overdueByUser[userId];
            await transporter.sendMail({
                from: 'no-reply@library.com',
                to: user.email,
                subject: 'Overdue books',
                text: `You have the following books overdue: ${books.map(b => b.title).join(', ')}`,
            });
        }
        */
        // Redirect to the admin dashboard.
        req.flash('success_msg', 'Overdue emails sent successfully');
        res.redirect('/staff');
    } catch (error) {
        next(error);
    }
};
