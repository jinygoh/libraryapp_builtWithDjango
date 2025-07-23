// This package contains the controller classes for the application.
package com.example.silentlibrary.controllers;

// Import necessary classes.
import com.example.silentlibrary.models.AuthenticationRequest;
import com.example.silentlibrary.models.AuthenticationResponse;
import com.example.silentlibrary.models.RegistrationRequest;
import com.example.silentlibrary.models.User;
import com.example.silentlibrary.repositories.UserRepository;
import com.example.silentlibrary.utils.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * This class is a REST controller that handles authentication-related requests.
 * The @RestController annotation marks this class as a REST controller.
 */
@RestController
public class AuthenticationController {

    // The AuthenticationManager is injected here to authenticate users.
    @Autowired
    private AuthenticationManager authenticationManager;

    // The UserDetailsService is injected here to load user-specific data.
    @Autowired
    private UserDetailsService userDetailsService;

    // The UserRepository is injected here to access user data.
    @Autowired
    private UserRepository userRepository;

    // The JwtUtil is injected here to work with JWTs.
    @Autowired
    private JwtUtil jwtUtil;

    /**
     * This method handles user registration requests.
     * It creates a new user and saves them to the database.
     * @param registrationRequest The request body, which contains the user's registration information.
     * @return A ResponseEntity indicating whether the registration was successful.
     */
    @PostMapping("/register")
    public ResponseEntity<?> registerUser(@RequestBody RegistrationRequest registrationRequest) {
        // Check if the username is already taken.
        if (userRepository.findByUsername(registrationRequest.getUsername()).isPresent()) {
            return ResponseEntity.badRequest().body("Username is already taken");
        }
        // Check if the email is already taken.
        if (userRepository.findByEmail(registrationRequest.getEmail()).isPresent()) {
            return ResponseEntity.badRequest().body("Email is already taken");
        }

        // Create a new User object.
        User user = new User();
        // Set the user's properties from the registration request.
        user.setUsername(registrationRequest.getUsername());
        user.setPassword(registrationRequest.getPassword());
        user.setEmail(registrationRequest.getEmail());
        user.setFirstName(registrationRequest.getFirstName());
        user.setLastName(registrationRequest.getLastName());
        user.setDateOfBirth(registrationRequest.getDateOfBirth());
        // Save the new user to the database.
        userRepository.save(user);

        // Return a success response.
        return ResponseEntity.ok("User registered successfully");
    }

    /**
     * This method handles authentication requests.
     * It authenticates the user and returns a JWT if the authentication is successful.
     * @param authenticationRequest The request body, which contains the user's credentials.
     * @return A ResponseEntity containing the JWT.
     * @throws Exception If the authentication fails.
     */
    @PostMapping("/authenticate")
    public ResponseEntity<?> createAuthenticationToken(@RequestBody AuthenticationRequest authenticationRequest) throws Exception {
        try {
            // Authenticate the user.
            authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(authenticationRequest.getUsername(), authenticationRequest.getPassword())
            );
        } catch (BadCredentialsException e) {
            // If the authentication fails, throw an exception.
            throw new Exception("Incorrect username or password", e);
        }

        // If the authentication is successful, load the user details.
        final UserDetails userDetails = userDetailsService.loadUserByUsername(authenticationRequest.getUsername());
        // Generate a JWT for the user.
        final String jwt = jwtUtil.generateToken(userDetails);

        // Return the JWT in the response.
        return ResponseEntity.ok(new AuthenticationResponse(jwt));
    }
}
