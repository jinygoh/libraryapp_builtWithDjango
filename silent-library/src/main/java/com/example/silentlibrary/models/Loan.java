// This package contains the model classes for the application.
package com.example.silentlibrary.models;

// Import necessary classes from the Jakarta Persistence API and java.util package.
import jakarta.persistence.*;
import java.util.Date;

/**
 * This class represents a Loan in the library system.
 * It is a JPA entity, which means it is mapped to a table in the database.
 */
@Entity
@Table(name = "loans")
public class Loan {

    // The primary key for the Loan entity.
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // A many-to-one relationship with the User entity.
    // This means that many loans can be associated with one user.
    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    // A many-to-one relationship with the Book entity.
    // This means that many loans can be associated with one book.
    @ManyToOne
    @JoinColumn(name = "book_id", nullable = false)
    private Book book;

    // The date the book was borrowed. It cannot be null.
    @Column(name = "borrow_date", nullable = false)
    private Date borrowDate;

    // The date the book is due to be returned. It cannot be null.
    @Column(name = "due_date", nullable = false)
    private Date dueDate;

    // The date the book was returned.
    @Column(name = "return_date")
    private Date returnDate;

    // The status of the loan (e.g., "borrowed", "returned"). It cannot be null.
    @Column(nullable = false)
    private String status;

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

    public Date getBorrowDate() {
        return borrowDate;
    }

    public void setBorrowDate(Date borrowDate) {
        this.borrowDate = borrowDate;
    }

    public Date getDueDate() {
        return dueDate;
    }

    public void setDueDate(Date dueDate) {
        this.dueDate = dueDate;
    }

    public Date getReturnDate() {
        return returnDate;
    }

    public void setReturnDate(Date returnDate) {
        this.returnDate = returnDate;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}
