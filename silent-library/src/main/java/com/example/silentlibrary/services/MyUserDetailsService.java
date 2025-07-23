// This package contains the service classes for the application.
package com.example.silentlibrary.services;

// Import necessary classes.
import com.example.silentlibrary.models.User;
import com.example.silentlibrary.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.ArrayList;

/**
 * This class implements the UserDetailsService interface from Spring Security.
 * It is used to load user-specific data.
 */
@Service
public class MyUserDetailsService implements UserDetailsService {

    // The UserRepository is injected here to allow access to the user data.
    @Autowired
    private UserRepository userRepository;

    /**
     * This method is called by Spring Security to load a user by their username.
     * @param username The username of the user to load.
     * @return A UserDetails object that contains the user's information.
     * @throws UsernameNotFoundException If the user is not found.
     */
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        // Find the user in the database by their username.
        User user = userRepository.findByUsername(username)
                // If the user is not found, throw an exception.
                .orElseThrow(() -> new UsernameNotFoundException("User not found with username: " + username));
        // Return a new UserDetails object with the user's username, password, and an empty list of authorities.
        return new org.springframework.security.core.userdetails.User(user.getUsername(), user.getPassword(), new ArrayList<>());
    }
}
