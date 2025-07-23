package com.example.silentlibrary.controllers;

import com.example.silentlibrary.models.User;
import com.example.silentlibrary.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/admin")
public class AdminController {

    @Autowired
    private UserRepository userRepository;

    @GetMapping("/users")
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    @PostMapping("/users/block/{userId}")
    public ResponseEntity<?> blockUser(@PathVariable Long userId) {
        return userRepository.findById(userId)
                .map(user -> {
                    user.setBlocked(true);
                    userRepository.save(user);
                    return ResponseEntity.ok().build();
                }).orElse(ResponseEntity.notFound().build());
    }

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
