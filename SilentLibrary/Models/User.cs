using Microsoft.AspNetCore.Identity;
using System;
using System.Collections.Generic;

namespace SilentLibrary.Models
{
    public class User : IdentityUser
    {
        public DateTime? DateOfBirth { get; set; }
        public bool IsBlocked { get; set; }

        public ICollection<Loan> Loans { get; set; }
        public ICollection<Review> Reviews { get; set; }
        public ICollection<Notification> Notifications { get; set; }
    }
}
