using System.Collections.Generic;

namespace SilentLibrary.Models
{
    public class DashboardViewModel
    {
        public IEnumerable<Loan> Loans { get; set; }
        public IEnumerable<Review> Reviews { get; set; }
    }
}
