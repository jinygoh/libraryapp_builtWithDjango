// This package contains the repository interfaces for the application.
package com.example.silentlibrary.repositories;

// Import necessary classes.
import com.example.silentlibrary.models.Review;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * This interface represents the repository for the Review entity.
 * It extends JpaRepository, which provides the basic CRUD operations for the Review entity.
 */
@Repository
public interface ReviewRepository extends JpaRepository<Review, Long> {

    /**
     * Finds all reviews for a given book.
     * @param bookId The ID of the book.
     * @return A list of reviews for the book.
     */
    List<Review> findByBookId(Long bookId);

    /**
     * Finds all reviews by a given user.
     * @param userId The ID of the user.
     * @return A list of reviews by the user.
     */
    List<Review> findByUserId(Long userId);
}
