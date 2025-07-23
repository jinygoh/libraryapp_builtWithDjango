// This package contains the model classes for the application.
package com.example.silentlibrary.models;

// Import necessary classes from the Jakarta Persistence API and java.util package.
import jakarta.persistence.*;
import java.util.Set;

/**
 * This class represents a Book in the library system.
 * It is a JPA entity, which means it is mapped to a table in the database.
 */
@Entity
@Table(name = "books")
public class Book {

    // The primary key for the Book entity.
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // The title of the book. It cannot be null.
    @Column(nullable = false)
    private String title;

    // The ISBN of the book. It cannot be null and must be unique.
    @Column(nullable = false, unique = true)
    private String isbn;

    // The total number of copies of the book. It cannot be null.
    @Column(name = "total_copies", nullable = false)
    private int totalCopies;

    // The number of available copies of the book. It cannot be null.
    @Column(name = "available_copies", nullable = false)
    private int availableCopies;

    // The URL of the book's image.
    private String image;

    // A many-to-many relationship with the Author entity.
    // The @ManyToMany annotation defines this relationship.
    // The @JoinTable annotation specifies the join table that connects the Book and Author tables.
    @ManyToMany
    @JoinTable(
            name = "books_authors",
            joinColumns = @JoinColumn(name = "book_id"),
            inverseJoinColumns = @JoinColumn(name = "author_id")
    )
    private Set<Author> authors;

    // A many-to-many relationship with the Genre entity.
    @ManyToMany
    @JoinTable(
            name = "books_genres",
            joinColumns = @JoinColumn(name = "book_id"),
            inverseJoinColumns = @JoinColumn(name = "genre_id")
    )
    private Set<Genre> genres;

    // --- Getters and Setters ---

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getIsbn() {
        return isbn;
    }

    public void setIsbn(String isbn) {
        this.isbn = isbn;
    }

    public int getTotalCopies() {
        return totalCopies;
    }

    public void setTotalCopies(int totalCopies) {
        this.totalCopies = totalCopies;
    }

    public int getAvailableCopies() {
        return availableCopies;
    }

    public void setAvailableCopies(int availableCopies) {
        this.availableCopies = availableCopies;
    }

    public String getImage() {
        return image;
    }

    public void setImage(String image) {
        this.image = image;
    }

    public Set<Author> getAuthors() {
        return authors;
    }

    public void setAuthors(Set<Author> authors) {
        this.authors = authors;
    }

    public Set<Genre> getGenres() {
        return genres;
    }

    public void setGenres(Set<Genre> genres) {
        this.genres = genres;
    }
}
