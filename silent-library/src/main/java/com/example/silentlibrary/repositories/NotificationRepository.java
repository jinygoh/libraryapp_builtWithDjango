// This package contains the repository interfaces for the application.
package com.example.silentlibrary.repositories;

// Import necessary classes.
import com.example.silentlibrary.models.Notification;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * This interface represents the repository for the Notification entity.
 * It extends JpaRepository, which provides the basic CRUD operations for the Notification entity.
 */
@Repository
public interface NotificationRepository extends JpaRepository<Notification, Long> {

    /**
     * Finds all notifications for a given user.
     * @param userId The ID of the user.
     * @return A list of notifications for the user.
     */
    List<Notification> findByUserId(Long userId);
}
