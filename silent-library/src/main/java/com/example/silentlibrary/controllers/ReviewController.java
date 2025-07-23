// This package contains the controller classes for the application.
package com.example.silentlibrary.controllers;

// Import necessary classes.
import com.example.silentlibrary.models.Book;
import com.example.silentlibrary.models.Review;
import com.example.silentlibrary.models.User;
import com.example.silentlibrary.repositories.BookRepository;
import com.example.silentlibrary.repositories.ReviewRepository;
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
 * This class is a REST controller that handles review-related requests.
 */
@RestController
@RequestMapping("/api/reviews")
public class ReviewController {

    // The ReviewRepository is injected here to access review data.
    @Autowired
    private ReviewRepository reviewRepository;

    // The BookRepository is injected here to access book data.
    @Autowired
    private BookRepository bookRepository;

    // The UserRepository is injected here to access user data.
    @Autowired
    private UserRepository userRepository;

    /**
     * This method handles GET requests to /api/reviews/book/{bookId}.
     * It returns a list of all reviews for the specified book.
     * @param bookId The ID of the book.
     * @return A list of reviews.
     */
    @GetMapping("/book/{bookId}")
    public List<Review> getReviewsByBook(@PathVariable Long bookId) {
        return reviewRepository.findByBookId(bookId);
    }

    /**
     * This method handles GET requests to /api/reviews/user.
     * It returns a list of all reviews for the currently authenticated user.
     * @return A list of reviews.
     */
    @GetMapping("/user")
    public List<Review> getMyReviews() {
        // Get the currently authenticated user's details.
        UserDetails userDetails = (UserDetails) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        // Find the user in the database.
        User user = userRepository.findByUsername(userDetails.getUsername()).get();
        // Return all reviews for the user.
        return reviewRepository.findByUserId(user.getId());
    }

    /**
     * This method handles POST requests to /api/reviews/book/{bookId}.
     * It allows the currently authenticated user to add a review for a book.
     * @param bookId The ID of the book to review.
     * @param review The request body, which contains the review's information.
     * @return A ResponseEntity indicating whether the review was added successfully.
     */
    @PostMapping("/book/{bookId}")
    public ResponseEntity<?> addReview(@PathVariable Long bookId, @RequestBody Review review) {
        // Get the currently authenticated user's details.
        UserDetails userDetails = (UserDetails) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        // Find the user in the database.
        User user = userRepository.findByUsername(userDetails.getUsername()).get();

        // Find the book in the database.
        Optional<Book> bookOptional = bookRepository.findById(bookId);
        // If the book is not found, return a 404 Not Found response.
        if (bookOptional.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        // Set the review's user, book, and review date.
        review.setUser(user);
        review.setBook(bookOptional.get());
        review.setReviewDate(new Date());
        // Save the new review to the database.
        reviewRepository.save(review);

        // Return a success response.
        return ResponseEntity.ok("Review added successfully");
    }
}
