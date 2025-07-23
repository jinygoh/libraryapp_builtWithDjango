// This package contains the repository interfaces for the application.
package com.example.silentlibrary.repositories;

// Import necessary classes.
import com.example.silentlibrary.models.Book;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * This interface represents the repository for the Book entity.
 * It extends JpaRepository, which provides the basic CRUD operations for the Book entity.
 */
@Repository
public interface BookRepository extends JpaRepository<Book, Long> {

    /**
     * Finds books by their title, ignoring case.
     * @param title The title to search for.
     * @return A list of books with matching titles.
     */
    List<Book> findByTitleContainingIgnoreCase(String title);

    /**
     * Finds books by the first or last name of their authors, ignoring case.
     * @param firstName The first name of the author to search for.
     * @param lastName The last name of the author to search for.
     * @return A list of books with matching authors.
     */
    List<Book> findByAuthorsFirstNameContainingIgnoreCaseOrAuthorsLastNameContainingIgnoreCase(String firstName, String lastName);

    /**
     * Finds books by their genre, ignoring case.
     * @param genre The genre to search for.
     * @return A list of books with matching genres.
     */
    List<Book> findByGenresGenreContainingIgnoreCase(String genre);
}
