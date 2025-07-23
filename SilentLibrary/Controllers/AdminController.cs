using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SilentLibrary.Data;
using SilentLibrary.Models;
using System.Linq;
using System.Threading.Tasks;

namespace SilentLibrary.Controllers
{
    [Authorize(Roles = "Admin")]
    public class AdminController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly UserManager<User> _userManager;

        public AdminController(ApplicationDbContext context, UserManager<User> userManager)
        {
            _context = context;
            _userManager = userManager;
        }

        public IActionResult Index()
        {
            return View();
        }

        public async Task<IActionResult> Books()
        {
            var books = await _context.Books.Include(b => b.BookAuthors).ThenInclude(ba => ba.Author).ToListAsync();
            return View(books);
        }

        public async Task<IActionResult> Users()
        {
            var users = await _userManager.Users.ToListAsync();
            return View(users);
        }

        [HttpGet]
        public IActionResult AddBook()
        {
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> AddBook(Book book, string authorFirstName, string authorLastName)
        {
            var author = await _context.Authors.FirstOrDefaultAsync(a => a.FirstName == authorFirstName && a.LastName == authorLastName);
            if (author == null)
            {
                author = new Author { FirstName = authorFirstName, LastName = authorLastName };
                _context.Authors.Add(author);
                await _context.SaveChangesAsync();
            }

            book.BookAuthors = new[] { new BookAuthor { AuthorId = author.Id } };
            _context.Books.Add(book);
            await _context.SaveChangesAsync();
            return RedirectToAction("Books");
        }

        [HttpGet]
        public async Task<IActionResult> EditBook(int id)
        {
            var book = await _context.Books.Include(b => b.BookAuthors).ThenInclude(ba => ba.Author).FirstOrDefaultAsync(b => b.Id == id);
            return View(book);
        }

        [HttpPost]
        public async Task<IActionResult> EditBook(Book book)
        {
            _context.Update(book);
            await _context.SaveChangesAsync();
            return RedirectToAction("Books");
        }

        [HttpGet]
        public async Task<IActionResult> DeleteBook(int id)
        {
            var book = await _context.Books.FindAsync(id);
            return View(book);
        }

        [HttpPost, ActionName("DeleteBook")]
        public async Task<IActionResult> DeleteBookConfirmed(int id)
        {
            var book = await _context.Books.FindAsync(id);
            _context.Books.Remove(book);
            await _context.SaveChangesAsync();
            return RedirectToAction("Books");
        }

        [HttpPost]
        public async Task<IActionResult> BlockUser(string id)
        {
            var user = await _userManager.FindByIdAsync(id);
            user.IsBlocked = true;
            await _userManager.UpdateAsync(user);
            return RedirectToAction("Users");
        }

        [HttpPost]
        public async Task<IActionResult> UnblockUser(string id)
        {
            var user = await _userManager.FindByIdAsync(id);
            user.IsBlocked = false;
            await _userManager.UpdateAsync(user);
            return RedirectToAction("Users");
        }

        [HttpPost]
        public async Task<IActionResult> SendOverdueEmails([FromServices] IEmailSender emailSender)
        {
            var overdueLoans = await _context.Loans
                .Include(l => l.User)
                .Include(l => l.Book)
                .Where(l => l.Status == Models.LoanStatus.Overdue)
                .ToListAsync();

            var usersToNotify = overdueLoans.Select(l => l.User).Distinct();

            foreach (var user in usersToNotify)
            {
                var userLoans = overdueLoans.Where(l => l.UserId == user.Id);
                var message = "You have the following books overdue:\n";
                foreach (var loan in userLoans)
                {
                    message += $"- {loan.Book.Title}\n";
                }
                await emailSender.SendEmailAsync(user.Email, "Overdue Books", message);
            }

            return RedirectToAction("Index");
        }
    }
}
