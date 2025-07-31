// This file contains the controller functions for book-related routes.
// The controller functions are responsible for handling the business logic of the application.
// They are called by the route handlers in the 'routes' directory.

const { Book, Author, Genre, Loan, Review, User, Sequelize } = require('../models');
const { Op } = Sequelize;

// This function handles book searches.
// It allows users to search for books by title, author, or genre.
exports.searchBooks = async (req, res, next) => {
  try {
    const { q } = req.query;
    let books = [];
    if (q) {
      // Find all books that match the search query.
      // The query searches the book title, author's first and last names, and genre.
      books = await Book.findAll({
        include: [
          { model: Author, where: { [Op.or]: [{ first_name: { [Op.iLike]: `%${q}%` } }, { last_name: { [Op.iLike]: `%${q}%` } }] } },
          { model: Genre, where: { genre: { [Op.iLike]: `%${q}%` } } },
        ],
        where: {
          title: { [Op.iLike]: `%${q}%` },
        },
      });
    } else {
      // If no search query is provided, find all books.
      books = await Book.findAll({ include: [Author, Genre]});
    }
    // Render the search view with the books data.
    res.render('search', { layout: 'base', books, query: q });
  } catch (error) {
    next(error);
  }
};

// This function renders the detail page for a specific book.
// It fetches the book's details and reviews from the database.
exports.getBookDetail = async (req, res, next) => {
  try {
    const { bookId } = req.params;
    // Find the book by its ID.
    const book = await Book.findByPk(bookId, {
      include: [Author, Genre],
    });
    // Find all reviews for the book.
    const reviews = await Review.findAll({ where: { bookId } });
    // Render the book detail view with the book and reviews data.
    res.render('book_detail', { layout: 'base', book, reviews });
  } catch (error) {
    next(error);
  }
};

// This function handles borrowing a book.
// It creates a new loan record for the user and the book.
exports.borrowBook = async (req, res, next) => {
  try {
    const { bookId } = req.params;
    const userId = req.session.user.id;
    const book = await Book.findByPk(bookId);
    if (book.available_copies > 0) {
      // Create a new loan record.
      await Loan.create({
        userId,
        bookId,
        due_date: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000), // 2 weeks from now
      });
      // Decrement the number of available copies.
      book.available_copies--;
      await book.save();
      req.flash('success_msg', 'Book borrowed successfully');
    } else {
        req.flash('error_msg', 'This book is not available for borrowing.');
    }
    // Redirect to the book detail page.
    res.redirect(`/book/${bookId}`);
  } catch (error) {
    next(error);
  }
};

// This function handles returning a book.
// It updates the loan record and increments the number of available copies.
exports.returnBook = async (req, res, next) => {
  try {
    const { loanId } = req.params;
    // Find the loan by its ID.
    const loan = await Loan.findByPk(loanId);
    // Update the loan status to 'returned'.
    loan.status = 'returned';
    loan.return_date = new Date();
    await loan.save();
    // Increment the number of available copies of the book.
    const book = await Book.findByPk(loan.bookId);
    book.available_copies++;
    await book.save();
    // Redirect to the user dashboard.
    req.flash('success_msg', 'Book returned successfully');
    res.redirect('/dashboard');
  } catch (error) {
    next(error);
  }
};

// This function handles submitting a review for a book.
// It creates a new review record for the user and the book.
exports.postReview = async (req, res, next) => {
    try {
        const { bookId } = req.params;
        const { rating, review_text } = req.body;
        const userId = req.session.user.id;

        // Check if the user has borrowed the book before allowing them to review it.
        const hasBorrowed = await Loan.findOne({ where: { userId, bookId } });
        if (!hasBorrowed) {
            // If the user has not borrowed the book, redirect to the book detail page with an error message.
            req.flash('error_msg', 'You can only review books you have borrowed.');
            return res.redirect(`/book/${bookId}`);
        }

        // Create a new review record.
        await Review.create({
            rating,
            review_text,
            userId,
            bookId,
        });
        // Redirect to the book detail page.
        req.flash('success_msg', 'Review submitted successfully');
        res.redirect(`/book/${bookId}`);
    } catch (error) {
        next(error);
    }
};
