using Microsoft.EntityFrameworkCore;
using SilentLibrary.Data;
using System;
using System.Linq;
using System.Threading.Tasks;

namespace SilentLibrary.Services
{
    public class FineService
    {
        private readonly ApplicationDbContext _context;

        public FineService(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task CalculateFines()
        {
            var overdueLoans = await _context.Loans
                .Where(l => l.Status == Models.LoanStatus.Borrowed && l.DueDate < DateTime.UtcNow)
                .ToListAsync();

            foreach (var loan in overdueLoans)
            {
                var daysOverdue = (DateTime.UtcNow - loan.DueDate).Days;
                var fineAmount = daysOverdue * 1.00m; // $1 per day

                var existingFine = await _context.Fines.FirstOrDefaultAsync(f => f.LoanId == loan.Id);
                if (existingFine == null)
                {
                    var fine = new Models.Fine
                    {
                        LoanId = loan.Id,
                        FineAmount = fineAmount,
                        FineDate = DateTime.UtcNow,
                        PaymentStatus = Models.FinePaymentStatus.Pending
                    };
                    _context.Fines.Add(fine);
                }
                else
                {
                    existingFine.FineAmount = fineAmount;
                }

                loan.Status = Models.LoanStatus.Overdue;
            }

            await _context.SaveChangesAsync();
        }
    }
}
