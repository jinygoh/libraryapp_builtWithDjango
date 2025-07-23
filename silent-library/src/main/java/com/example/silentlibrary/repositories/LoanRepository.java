// This package contains the repository interfaces for the application.
package com.example.silentlibrary.repositories;

// Import necessary classes.
import com.example.silentlibrary.models.Loan;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * This interface represents the repository for the Loan entity.
 * It extends JpaRepository, which provides the basic CRUD operations for the Loan entity.
 */
@Repository
public interface LoanRepository extends JpaRepository<Loan, Long> {

    /**
     * Finds all loans for a given user.
     * @param userId The ID of the user.
     * @return A list of loans for the user.
     */
    List<Loan> findByUserId(Long userId);
}
