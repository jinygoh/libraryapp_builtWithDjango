using System;
using System.ComponentModel.DataAnnotations;

namespace SilentLibrary.Models
{
    public class Notification
    {
        public int Id { get; set; }

        [Required]
        public DateTime Timestamp { get; set; }

        [Required]
        [StringLength(512)]
        public string NotificationText { get; set; }

        [Required]
        public string UserId { get; set; }
        public User User { get; set; }
    }
}
