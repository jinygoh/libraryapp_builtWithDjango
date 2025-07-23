package com.example.silentlibrary.repositories;

import com.example.silentlibrary.models.Book;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface BookRepository extends JpaRepository<Book, Long> {
    List<Book> findByTitleContainingIgnoreCase(String title);
    List<Book> findByAuthorsFirstNameContainingIgnoreCaseOrAuthorsLastNameContainingIgnoreCase(String firstName, String lastName);
    List<Book> findByGenresGenreContainingIgnoreCase(String genre);
}
