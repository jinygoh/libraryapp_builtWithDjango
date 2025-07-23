// This package contains the repository interfaces for the application.
package com.example.silentlibrary.repositories;

// Import necessary classes.
import com.example.silentlibrary.models.Author;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * This interface represents the repository for the Author entity.
 * It extends JpaRepository, which provides the basic CRUD operations for the Author entity.
 */
@Repository
public interface AuthorRepository extends JpaRepository<Author, Long> {
}
