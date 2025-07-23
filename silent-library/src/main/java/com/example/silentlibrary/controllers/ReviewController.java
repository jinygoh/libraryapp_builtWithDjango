package com.example.silentlibrary.controllers;

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

@RestController
@RequestMapping("/api/reviews")
public class ReviewController {

    @Autowired
    private ReviewRepository reviewRepository;

    @Autowired
    private BookRepository bookRepository;

    @Autowired
    private UserRepository userRepository;

    @GetMapping("/book/{bookId}")
    public List<Review> getReviewsByBook(@PathVariable Long bookId) {
        return reviewRepository.findByBookId(bookId);
    }

    @GetMapping("/user")
    public List<Review> getMyReviews() {
        UserDetails userDetails = (UserDetails) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        User user = userRepository.findByUsername(userDetails.getUsername()).get();
        return reviewRepository.findByUserId(user.getId());
    }

    @PostMapping("/book/{bookId}")
    public ResponseEntity<?> addReview(@PathVariable Long bookId, @RequestBody Review review) {
        UserDetails userDetails = (UserDetails) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        User user = userRepository.findByUsername(userDetails.getUsername()).get();

        Optional<Book> bookOptional = bookRepository.findById(bookId);
        if (bookOptional.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        review.setUser(user);
        review.setBook(bookOptional.get());
        review.setReviewDate(new Date());
        reviewRepository.save(review);

        return ResponseEntity.ok("Review added successfully");
    }
}
