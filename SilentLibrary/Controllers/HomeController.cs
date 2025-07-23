using Microsoft.AspNetCore.Mvc;

namespace SilentLibrary.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
