// This package contains the model classes for the application.
package com.example.silentlibrary.models;

// Import necessary classes from the Jakarta Persistence API.
import jakarta.persistence.*;

/**
 * This class represents a Genre in the library system.
 * It is a JPA entity, which means it is mapped to a table in the database.
 */
@Entity
@Table(name = "genres")
public class Genre {

    // The primary key for the Genre entity.
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // The name of the genre. It cannot be null and must be unique.
    @Column(nullable = false, unique = true)
    private String genre;

    // --- Getters and Setters ---

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getGenre() {
        return genre;
    }

    public void setGenre(String genre) {
        this.genre = genre;
    }
}
