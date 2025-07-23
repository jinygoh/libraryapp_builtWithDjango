// This package contains the controller classes for the application.
package com.example.silentlibrary.controllers;

// Import necessary classes.
import com.example.silentlibrary.models.Book;
import com.example.silentlibrary.repositories.BookRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * This class is a REST controller that handles book-related requests.
 */
@RestController
@RequestMapping("/api/books")
public class BookController {

    // The BookRepository is injected here to access book data.
    @Autowired
    private BookRepository bookRepository;

    /**
     * This method handles GET requests to /api/books.
     * It returns a list of all books in the database.
     * @return A list of all books.
     */
    @GetMapping
    public List<Book> getAllBooks() {
        return bookRepository.findAll();
    }

    /**
     * This method handles GET requests to /api/books/{id}.
     * It returns the book with the specified ID.
     * @param bookId The ID of the book to return.
     * @return A ResponseEntity containing the book, or a 404 Not Found response if the book is not found.
     */
    @GetMapping("/{id}")
    public ResponseEntity<Book> getBookById(@PathVariable(value = "id") Long bookId) {
        return bookRepository.findById(bookId)
                .map(book -> ResponseEntity.ok().body(book))
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * This method handles POST requests to /api/books.
     * It creates a new book and saves it to the database.
     * @param book The request body, which contains the book's information.
     * @return The newly created book.
     */
    @PostMapping
    public Book createBook(@RequestBody Book book) {
        return bookRepository.save(book);
    }

    /**
     * This method handles PUT requests to /api/books/{id}.
     * It updates the book with the specified ID.
     * @param bookId The ID of the book to update.
     * @param bookDetails The request body, which contains the updated book information.
     * @return A ResponseEntity containing the updated book, or a 404 Not Found response if the book is not found.
     */
    @PutMapping("/{id}")
    public ResponseEntity<Book> updateBook(@PathVariable(value = "id") Long bookId, @RequestBody Book bookDetails) {
        return bookRepository.findById(bookId)
                .map(book -> {
                    book.setTitle(bookDetails.getTitle());
                    book.setIsbn(bookDetails.getIsbn());
                    book.setTotalCopies(bookDetails.getTotalCopies());
                    book.setAvailableCopies(bookDetails.getAvailableCopies());
                    book.setImage(bookDetails.getImage());
                    book.setAuthors(bookDetails.getAuthors());
                    book.setGenres(bookDetails.getGenres());
                    Book updatedBook = bookRepository.save(book);
                    return ResponseEntity.ok().body(updatedBook);
                }).orElse(ResponseEntity.notFound().build());
    }

    /**
     * This method handles DELETE requests to /api/books/{id}.
     * It deletes the book with the specified ID.
     * @param bookId The ID of the book to delete.
     * @return A ResponseEntity indicating whether the deletion was successful.
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteBook(@PathVariable(value = "id") Long bookId) {
        return bookRepository.findById(bookId)
                .map(book -> {
                    bookRepository.delete(book);
                    return ResponseEntity.ok().build();
                }).orElse(ResponseEntity.notFound().build());
    }

    /**
     * This method handles GET requests to /api/books/search.
     * It searches for books by title.
     * @param query The search query.
     * @return A list of books that match the search query.
     */
    @GetMapping("/search")
    public List<Book> searchBooks(@RequestParam("q") String query) {
        return bookRepository.findByTitleContainingIgnoreCase(query);
    }
}
