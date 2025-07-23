// This package contains the controller classes for the application.
package com.example.silentlibrary.controllers;

// Import necessary classes.
import com.example.silentlibrary.models.Book;
import com.example.silentlibrary.models.Loan;
import com.example.silentlibrary.models.User;
import com.example.silentlibrary.repositories.BookRepository;
import com.example.silentlibrary.repositories.LoanRepository;
import com.example.silentlibrary.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.List;
import java.util.Optional;

/**
 * This class is a REST controller that handles loan-related requests.
 */
@RestController
@RequestMapping("/api/loans")
public class LoanController {

    // The LoanRepository is injected here to access loan data.
    @Autowired
    private LoanRepository loanRepository;

    // The BookRepository is injected here to access book data.
    @Autowired
    private BookRepository bookRepository;

    // The UserRepository is injected here to access user data.
    @Autowired
    private UserRepository userRepository;

    /**
     * This method handles GET requests to /api/loans.
     * It returns a list of all loans for the currently authenticated user.
     * @return A list of loans.
     */
    @GetMapping
    public List<Loan> getMyLoans() {
        // Get the currently authenticated user's details.
        UserDetails userDetails = (UserDetails) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        // Find the user in the database.
        User user = userRepository.findByUsername(userDetails.getUsername()).get();
        // Return all loans for the user.
        return loanRepository.findByUserId(user.getId());
    }

    /**
     * This method handles POST requests to /api/loans/borrow/{bookId}.
     * It allows the currently authenticated user to borrow a book.
     * @param bookId The ID of the book to borrow.
     * @return A ResponseEntity indicating whether the book was borrowed successfully.
     */
    @PostMapping("/borrow/{bookId}")
    public ResponseEntity<?> borrowBook(@PathVariable Long bookId) {
        // Get the currently authenticated user's details.
        UserDetails userDetails = (UserDetails) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        // Find the user in the database.
        User user = userRepository.findByUsername(userDetails.getUsername()).get();

        // Check if the user is blocked.
        if (user.isBlocked()) {
            return ResponseEntity.badRequest().body("User is blocked");
        }

        // Find the book in the database.
        Optional<Book> bookOptional = bookRepository.findById(bookId);
        // If the book is not found, return a 404 Not Found response.
        if (bookOptional.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        // Get the book from the Optional.
        Book book = bookOptional.get();
        // Check if the book is available.
        if (book.getAvailableCopies() <= 0) {
            return ResponseEntity.badRequest().body("Book is not available");
        }

        // Create a new Loan object.
        Loan loan = new Loan();
        // Set the loan's properties.
        loan.setUser(user);
        loan.setBook(book);
        loan.setBorrowDate(new Date());
        loan.setDueDate(new Date(System.currentTimeMillis() + 1000 * 60 * 60 * 24 * 14)); // 14 days
        loan.setStatus("borrowed");
        // Save the new loan to the database.
        loanRepository.save(loan);

        // Decrement the number of available copies of the book.
        book.setAvailableCopies(book.getAvailableCopies() - 1);
        // Save the updated book to the database.
        bookRepository.save(book);

        // Return a success response.
        return ResponseEntity.ok("Book borrowed successfully");
    }

    /**
     * This method handles POST requests to /api/loans/return/{loanId}.
     * It allows the currently authenticated user to return a book.
     * @param loanId The ID of the loan to return.
     * @return A ResponseEntity indicating whether the book was returned successfully.
     */
    @PostMapping("/return/{loanId}")
    public ResponseEntity<?> returnBook(@PathVariable Long loanId) {
        // Find the loan in the database.
        Optional<Loan> loanOptional = loanRepository.findById(loanId);
        // If the loan is not found, return a 404 Not Found response.
        if (loanOptional.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        // Get the loan from the Optional.
        Loan loan = loanOptional.get();
        // Check if the book has already been returned.
        if (loan.getStatus().equals("returned")) {
            return ResponseEntity.badRequest().body("Book already returned");
        }

        // Set the loan's return date and status.
        loan.setReturnDate(new Date());
        loan.setStatus("returned");
        // Save the updated loan to the database.
        loanRepository.save(loan);

        // Get the book from the loan.
        Book book = loan.getBook();
        // Increment the number of available copies of the book.
        book.setAvailableCopies(book.getAvailableCopies() + 1);
        // Save the updated book to the database.
        bookRepository.save(book);

        // Return a success response.
        return ResponseEntity.ok("Book returned successfully");
    }
}
