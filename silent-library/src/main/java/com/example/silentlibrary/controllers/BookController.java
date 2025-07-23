package com.example.silentlibrary.controllers;

import com.example.silentlibrary.models.Book;
import com.example.silentlibrary.repositories.BookRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/books")
public class BookController {

    @Autowired
    private BookRepository bookRepository;

    @GetMapping
    public List<Book> getAllBooks() {
        return bookRepository.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Book> getBookById(@PathVariable(value = "id") Long bookId) {
        return bookRepository.findById(bookId)
                .map(book -> ResponseEntity.ok().body(book))
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public Book createBook(@RequestBody Book book) {
        return bookRepository.save(book);
    }

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

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteBook(@PathVariable(value = "id") Long bookId) {
        return bookRepository.findById(bookId)
                .map(book -> {
                    bookRepository.delete(book);
                    return ResponseEntity.ok().build();
                }).orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/search")
    public List<Book> searchBooks(@RequestParam("q") String query) {
        return bookRepository.findByTitleContainingIgnoreCase(query);
    }
}
