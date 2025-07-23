using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace SilentLibrary.Models
{
    public enum FinePaymentStatus
    {
        Pending,
        Paid,
        Waived
    }

    public class Fine
    {
        public int Id { get; set; }

        [Required]
        [Column(TypeName = "decimal(10, 2)")]
        public decimal FineAmount { get; set; }

        [Required]
        public FinePaymentStatus PaymentStatus { get; set; }

        [Required]
        public DateTime FineDate { get; set; }

        public DateTime? PaymentDate { get; set; }

        [Required]
        public int LoanId { get; set; }
        public Loan Loan { get; set; }
    }
}
