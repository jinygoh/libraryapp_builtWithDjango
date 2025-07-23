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
    [Authorize]
    public class DashboardController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly UserManager<User> _userManager;

        public DashboardController(ApplicationDbContext context, UserManager<User> userManager)
        {
            _context = context;
            _userManager = userManager;
        }

        public async Task<IActionResult> Index()
        {
            var user = await _userManager.GetUserAsync(User);
            var loans = await _context.Loans.Include(l => l.Book).Where(l => l.UserId == user.Id).ToListAsync();
            var reviews = await _context.Reviews.Include(r => r.Book).Where(r => r.UserId == user.Id).ToListAsync();

            var model = new DashboardViewModel
            {
                Loans = loans,
                Reviews = reviews
            };

            return View(model);
        }

        [HttpPost]
        public async Task<IActionResult> ReturnBook(int loanId)
        {
            var loan = await _context.Loans.Include(l => l.Book).FirstOrDefaultAsync(l => l.Id == loanId);
            if (loan != null && loan.Status == LoanStatus.Borrowed)
            {
                loan.Status = LoanStatus.Returned;
                loan.ReturnDate = DateTime.UtcNow;
                loan.Book.AvailableCopies++;
                await _context.SaveChangesAsync();
            }

            return RedirectToAction("Index");
        }
    }
}
