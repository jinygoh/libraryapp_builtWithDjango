// This package contains the model classes for the application.
package com.example.silentlibrary.models;

// Import necessary classes from the Jakarta Persistence API and java.math and java.util packages.
import jakarta.persistence.*;
import java.math.BigDecimal;
import java.util.Date;

/**
 * This class represents a Fine in the library system.
 * It is a JPA entity, which means it is mapped to a table in the database.
 */
@Entity
@Table(name = "fines")
public class Fine {

    // The primary key for the Fine entity.
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // A one-to-one relationship with the Loan entity.
    // This means that each fine is associated with one loan.
    @OneToOne
    @JoinColumn(name = "loan_id", nullable = false)
    private Loan loan;

    // The amount of the fine. It cannot be null.
    @Column(name = "fine_amount", nullable = false)
    private BigDecimal fineAmount;

    // The payment status of the fine (e.g., "paid", "unpaid"). It cannot be null.
    @Column(name = "payment_status", nullable = false)
    private String paymentStatus;

    // The date the fine was issued. It cannot be null.
    @Column(name = "fine_date", nullable = false)
    private Date fineDate;

    // The date the fine was paid.
    @Column(name = "payment_date")
    private Date paymentDate;

    // --- Getters and Setters ---

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Loan getLoan() {
        return loan;
    }

    public void setLoan(Loan loan) {
        this.loan = loan;
    }

    public BigDecimal getFineAmount() {
        return fineAmount;
    }

    public void setFineAmount(BigDecimal fineAmount) {
        this.fineAmount = fineAmount;
    }

    public String getPaymentStatus() {
        return paymentStatus;
    }

    public void setPaymentStatus(String paymentStatus) {
        this.paymentStatus = paymentStatus;
    }

    public Date getFineDate() {
        return fineDate;
    }

    public void setFineDate(Date fineDate) {
        this.fineDate = fineDate;
    }

    public Date getPaymentDate() {
        return paymentDate;
    }

    public void setPaymentDate(Date paymentDate) {
        this.paymentDate = paymentDate;
    }
}
