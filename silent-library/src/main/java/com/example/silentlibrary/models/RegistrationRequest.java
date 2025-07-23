// This package contains the model classes for the application.
package com.example.silentlibrary.models;

import java.util.Date;

/**
 * This class represents the request body for a user registration request.
 * It contains all the information needed to create a new user.
 */
public class RegistrationRequest {
    // The username of the new user.
    private String username;
    // The password of the new user.
    private String password;
    // The email of the new user.
    private String email;
    // The first name of the new user.
    private String firstName;
    // The last name of the new user.
    private String lastName;
    // The date of birth of the new user.
    private Date dateOfBirth;

    // --- Getters and Setters ---

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
}
