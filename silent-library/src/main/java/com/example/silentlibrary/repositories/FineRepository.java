// This package contains the repository interfaces for the application.
package com.example.silentlibrary.repositories;

// Import necessary classes.
import com.example.silentlibrary.models.Fine;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * This interface represents the repository for the Fine entity.
 * It extends JpaRepository, which provides the basic CRUD operations for the Fine entity.
 */
@Repository
public interface FineRepository extends JpaRepository<Fine, Long> {
}
