// This package contains the model classes for the application.
package com.example.silentlibrary.models;

/**
 * This class represents the response body for a successful authentication request.
 * It contains the JSON Web Token (JWT) that is sent back to the client.
 */
public class AuthenticationResponse {
    // The JWT.
    private final String jwt;

    /**
     * Constructor for the AuthenticationResponse class.
     * @param jwt The JWT to be included in the response.
     */
    public AuthenticationResponse(String jwt) {
        this.jwt = jwt;
    }

    /**
     * Getter for the JWT.
     * @return The JWT.
     */
    public String getJwt() {
        return jwt;
    }
}
