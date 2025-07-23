using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace SilentLibrary.Models
{
    public class Genre
    {
        public int Id { get; set; }

        [Required]
        [StringLength(50)]
        public string Name { get; set; }

        public ICollection<BookGenre> BookGenres { get; set; }
    }
}
