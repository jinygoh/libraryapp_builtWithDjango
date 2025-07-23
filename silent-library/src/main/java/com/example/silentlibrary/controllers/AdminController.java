// This package contains the controller classes for the application.
package com.example.silentlibrary.controllers;

// Import necessary classes.
import com.example.silentlibrary.models.User;
import com.example.silentlibrary.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * This class is a REST controller that handles admin-related requests.
 */
@RestController
@RequestMapping("/api/admin")
public class AdminController {

    // The UserRepository is injected here to access user data.
    @Autowired
    private UserRepository userRepository;

    /**
     * This method handles GET requests to /api/admin/users.
     * It returns a list of all users in the database.
     * @return A list of all users.
     */
    @GetMapping("/users")
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    /**
     * This method handles POST requests to /api/admin/users/block/{userId}.
     * It blocks the user with the specified ID.
     * @param userId The ID of the user to block.
     * @return A ResponseEntity indicating whether the user was blocked successfully.
     */
    @PostMapping("/users/block/{userId}")
    public ResponseEntity<?> blockUser(@PathVariable Long userId) {
        return userRepository.findById(userId)
                .map(user -> {
                    user.setBlocked(true);
                    userRepository.save(user);
                    return ResponseEntity.ok().build();
                }).orElse(ResponseEntity.notFound().build());
    }

    /**
     * This method handles POST requests to /api/admin/users/unblock/{userId}.
     * It unblocks the user with the specified ID.
     * @param userId The ID of the user to unblock.
     * @return A ResponseEntity indicating whether the user was unblocked successfully.
     */
    @PostMapping("/users/unblock/{userId}")
    public ResponseEntity<?> unblockUser(@PathVariable Long userId) {
        return userRepository.findById(userId)
                .map(user -> {
                    user.setBlocked(false);
                    userRepository.save(user);
                    return ResponseEntity.ok().build();
                }).orElse(ResponseEntity.notFound().build());
    }
}
