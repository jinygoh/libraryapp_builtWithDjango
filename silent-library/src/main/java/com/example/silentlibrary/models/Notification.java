// This package contains the model classes for the application.
package com.example.silentlibrary.models;

// Import necessary classes from the Jakarta Persistence API and java.util package.
import jakarta.persistence.*;
import java.util.Date;

/**
 * This class represents a Notification in the library system.
 * It is a JPA entity, which means it is mapped to a table in the database.
 */
@Entity
@Table(name = "notifications")
public class Notification {

    // The primary key for the Notification entity.
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // A many-to-one relationship with the User entity.
    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    // The text of the notification. It cannot be null.
    @Column(name = "notification_text", nullable = false)
    private String notificationText;

    // The timestamp of when the notification was created. It cannot be null.
    @Column(nullable = false)
    private Date timestamp;

    // --- Getters and Setters ---

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public String getNotificationText() {
        return notificationText;
    }

    public void setNotificationText(String notificationText) {
        this.notificationText = notificationText;
    }

    public Date getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Date timestamp) {
        this.timestamp = timestamp;
    }
}
