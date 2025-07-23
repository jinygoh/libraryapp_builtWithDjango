using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SilentLibrary.Data;
using SilentLibrary.Models;
using System.Linq;
using System.Threading.Tasks;

namespace SilentLibrary.Controllers
{
    public class BookController : Controller
    {
        private readonly ApplicationDbContext _context;

        public BookController(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<IActionResult> Search(string query)
        {
            var books = _context.Books.Include(b => b.BookAuthors).ThenInclude(ba => ba.Author).AsQueryable();

            if (!string.IsNullOrEmpty(query))
            {
                books = books.Where(b => b.Title.Contains(query) ||
                                         b.BookAuthors.Any(ba => ba.Author.FirstName.Contains(query) || ba.Author.LastName.Contains(query)));
            }

            return View(await books.ToListAsync());
        }

        public async Task<IActionResult> Details(int id)
        {
            var book = await _context.Books
                .Include(b => b.BookAuthors).ThenInclude(ba => ba.Author)
                .Include(b => b.BookGenres).ThenInclude(bg => bg.Genre)
                .Include(b => b.Reviews).ThenInclude(r => r.User)
                .FirstOrDefaultAsync(m => m.Id == id);

            if (book == null)
            {
                return NotFound();
            }

            return View(book);
        }

        [HttpPost]
        public async Task<IActionResult> AddReview(int bookId, int rating, string reviewText)
        {
            var user = await _userManager.GetUserAsync(User);
            var review = new Review
            {
                BookId = bookId,
                UserId = user.Id,
                Rating = rating,
                ReviewText = reviewText,
                ReviewDate = DateTime.UtcNow
            };

            _context.Reviews.Add(review);
            await _context.SaveChangesAsync();

            return RedirectToAction("Details", new { id = bookId });
        }

        [HttpPost]
        public async Task<IActionResult> BorrowBook(int bookId)
        {
            var user = await _userManager.GetUserAsync(User);
            var book = await _context.Books.FindAsync(bookId);

            if (book.AvailableCopies > 0)
            {
                book.AvailableCopies--;
                var loan = new Loan
                {
                    BookId = bookId,
                    UserId = user.Id,
                    BorrowDate = DateTime.UtcNow,
                    DueDate = DateTime.UtcNow.AddDays(14),
                    Status = LoanStatus.Borrowed
                };
                _context.Loans.Add(loan);
                await _context.SaveChangesAsync();
            }

            return RedirectToAction("Details", new { id = bookId });
        }
    }
}
