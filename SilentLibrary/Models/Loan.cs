using System;
using System.ComponentModel.DataAnnotations;

namespace SilentLibrary.Models
{
    public enum LoanStatus
    {
        Borrowed,
        Returned,
        Overdue
    }

    public class Loan
    {
        public int Id { get; set; }

        [Required]
        public DateTime BorrowDate { get; set; }

        [Required]
        public DateTime DueDate { get; set; }

        public DateTime? ReturnDate { get; set; }

        [Required]
        public LoanStatus Status { get; set; }

        [Required]
        public string UserId { get; set; }
        public User User { get; set; }

        [Required]
        public int BookId { get; set; }
        public Book Book { get; set; }

        public ICollection<Fine> Fines { get; set; }
    }
}
