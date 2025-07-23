using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace SilentLibrary.Models
{
    public class Book
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Title { get; set; }

        [Required]
        [StringLength(17)]
        public string Isbn { get; set; }

        [Required]
        public int TotalCopies { get; set; }

        [Required]
        public int AvailableCopies { get; set; }

        public string Image { get; set; }

        public ICollection<BookAuthor> BookAuthors { get; set; }
        public ICollection<BookGenre> BookGenres { get; set; }
        public ICollection<Loan> Loans { get; set; }
        public ICollection<Review> Reviews { get; set; }
    }
}
