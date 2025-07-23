// This package contains the repository interfaces for the application.
package com.example.silentlibrary.repositories;

// Import necessary classes.
import com.example.silentlibrary.models.Genre;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * This interface represents the repository for the Genre entity.
 * It extends JpaRepository, which provides the basic CRUD operations for the Genre entity.
 */
@Repository
public interface GenreRepository extends JpaRepository<Genre, Long> {
}
