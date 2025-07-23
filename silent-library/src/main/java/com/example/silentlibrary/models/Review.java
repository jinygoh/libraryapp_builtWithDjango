// This package contains the model classes for the application.
package com.example.silentlibrary.models;

// Import necessary classes from the Jakarta Persistence API and java.util package.
import jakarta.persistence.*;
import java.util.Date;

/**
 * This class represents a Review in the library system.
 * It is a JPA entity, which means it is mapped to a table in the database.
 */
@Entity
@Table(name = "reviews")
public class Review {

    // The primary key for the Review entity.
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // A many-to-one relationship with the User entity.
    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    // A many-to-one relationship with the Book entity.
    @ManyToOne
    @JoinColumn(name = "book_id", nullable = false)
    private Book book;

    // The rating given in the review. It cannot be null.
    @Column(nullable = false)
    private int rating;

    // The text of the review.
    @Column(name = "review_text", columnDefinition = "TEXT")
    private String reviewText;

    // The date the review was submitted. It cannot be null.
    @Column(name = "review_date", nullable = false)
    private Date reviewDate;

    // --- Getters and Setters ---

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public Book getBook() {
        return book;
    }

    public void setBook(Book book) {
        this.book = book;
    }

    public int getRating() {
        return rating;
    }

    public void setRating(int rating) {
        this.rating = rating;
    }

    public String getReviewText() {
        return reviewText;
    }

    public void setReviewText(String reviewText) {
        this.reviewText = reviewText;
    }

    public Date getReviewDate() {
        return reviewDate;
    }

    public void setReviewDate(Date reviewDate) {
        this.reviewDate = reviewDate;
    }
}
