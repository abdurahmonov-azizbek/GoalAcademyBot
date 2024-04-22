using GoalAcademyServerApp.DbContexts;
using GoalAcademyServerApp.Models;
using Microsoft.AspNetCore.Mvc;

namespace GoalAcademyServerApp.Controllers;

[ApiController]
[Route("api/[controller]")]
public class PollsController(AppDbContext dbContext) : ControllerBase
{
    [HttpPost]
    public IActionResult Create([FromBody] Poll poll)
    {
        poll.Id = Guid.NewGuid();
        dbContext.Polls.Add(poll);
        dbContext.SaveChanges();
        return Ok(poll);
    }
}

