using System.Threading.Tasks;

namespace SilentLibrary.Services
{
    public interface IEmailSender
    {
        Task SendEmailAsync(string email, string subject, string message);
    }

    public class EmailSender : IEmailSender
    {
        public Task SendEmailAsync(string email, string subject, string message)
        {
            // Plug in your email sending logic here.
            return Task.CompletedTask;
        }
    }
}
