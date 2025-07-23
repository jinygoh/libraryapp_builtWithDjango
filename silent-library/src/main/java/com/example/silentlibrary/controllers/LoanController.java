package com.example.silentlibrary.controllers;

import com.example.silentlibrary.models.Book;
import com.example.silentlibrary.models.Loan;
import com.example.silentlibrary.models.User;
import com.example.silentlibrary.repositories.BookRepository;
import com.example.silentlibrary.repositories.LoanRepository;
import com.example.silentlibrary.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/loans")
public class LoanController {

    @Autowired
    private LoanRepository loanRepository;

    @Autowired
    private BookRepository bookRepository;

    @Autowired
    private UserRepository userRepository;

    @GetMapping
    public List<Loan> getMyLoans() {
        UserDetails userDetails = (UserDetails) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        User user = userRepository.findByUsername(userDetails.getUsername()).get();
        return loanRepository.findByUserId(user.getId());
    }

    @PostMapping("/borrow/{bookId}")
    public ResponseEntity<?> borrowBook(@PathVariable Long bookId) {
        UserDetails userDetails = (UserDetails) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        User user = userRepository.findByUsername(userDetails.getUsername()).get();

        if (user.isBlocked()) {
            return ResponseEntity.badRequest().body("User is blocked");
        }

        Optional<Book> bookOptional = bookRepository.findById(bookId);
        if (bookOptional.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        Book book = bookOptional.get();
        if (book.getAvailableCopies() <= 0) {
            return ResponseEntity.badRequest().body("Book is not available");
        }

        Loan loan = new Loan();
        loan.setUser(user);
        loan.setBook(book);
        loan.setBorrowDate(new Date());
        loan.setDueDate(new Date(System.currentTimeMillis() + 1000 * 60 * 60 * 24 * 14)); // 14 days
        loan.setStatus("borrowed");
        loanRepository.save(loan);

        book.setAvailableCopies(book.getAvailableCopies() - 1);
        bookRepository.save(book);

        return ResponseEntity.ok("Book borrowed successfully");
    }

    @PostMapping("/return/{loanId}")
    public ResponseEntity<?> returnBook(@PathVariable Long loanId) {
        Optional<Loan> loanOptional = loanRepository.findById(loanId);
        if (loanOptional.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        Loan loan = loanOptional.get();
        if (loan.getStatus().equals("returned")) {
            return ResponseEntity.badRequest().body("Book already returned");
        }

        loan.setReturnDate(new Date());
        loan.setStatus("returned");
        loanRepository.save(loan);

        Book book = loan.getBook();
        book.setAvailableCopies(book.getAvailableCopies() + 1);
        bookRepository.save(book);

        return ResponseEntity.ok("Book returned successfully");
    }
}
