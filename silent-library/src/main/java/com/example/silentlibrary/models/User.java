// This package contains the model classes for the application.
package com.example.silentlibrary.models;

// Import necessary classes from the Jakarta Persistence API.
import jakarta.persistence.*;
import java.util.Date;

/**
 * This class represents a User in the library system.
 * It is a JPA entity, which means it is mapped to a table in the database.
 * The @Entity annotation marks this class as a JPA entity.
 * The @Table annotation specifies the name of the database table to be used for mapping.
 */
@Entity
@Table(name = "users")
public class User {

    // The primary key for the User entity.
    @Id
    // The value of the primary key is generated automatically.
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // The username of the user. It cannot be null and must be unique.
    @Column(nullable = false, unique = true)
    private String username;

    // The password of the user. It cannot be null.
    @Column(nullable = false)
    private String password;

    // The email of the user. It cannot be null and must be unique.
    @Column(nullable = false, unique = true)
    private String email;

    // The first name of the user.
    @Column(name = "first_name")
    private String firstName;

    // The last name of the user.
    @Column(name = "last_name")
    private String lastName;

    // The date of birth of the user.
    @Column(name = "date_of_birth")
    private Date dateOfBirth;

    // A flag indicating whether the user is blocked.
    @Column(name = "is_blocked")
    private boolean isBlocked = false;

    // --- Getters and Setters ---

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public Date getDateOfBirth() {
        return dateOfBirth;
    }

    public void setDateOfBirth(Date dateOfBirth) {
        this.dateOfBirth = dateOfBirth;
    }

    public boolean isBlocked() {
        return isBlocked;
    }

    public void setBlocked(boolean blocked) {
        isBlocked = blocked;
    }
}
