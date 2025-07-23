// This package contains the model classes for the application.
package com.example.silentlibrary.models;

/**
 * This class represents the request body for an authentication request.
 * It contains the username and password of the user trying to authenticate.
 */
public class AuthenticationRequest {
    // The username of the user.
    private String username;
    // The password of the user.
    private String password;

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
}
