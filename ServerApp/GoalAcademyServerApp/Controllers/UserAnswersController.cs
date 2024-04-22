using GoalAcademyServerApp.DbContexts;
using GoalAcademyServerApp.Models;
using Microsoft.AspNetCore.Mvc;

namespace GoalAcademyServerApp.Controllers;

[ApiController]
[Route("api/[controller]")]
public class UserAnswersController(AppDbContext dbContext) : ControllerBase
{
    [HttpPost]
    public IActionResult Create([FromBody] UserAnswer userAnswer)
    {
        userAnswer.Id = Guid.NewGuid();
        dbContext.UserAnswers.Add(userAnswer);
        dbContext.SaveChanges();
        return Ok(userAnswer);
    }

    [HttpGet("{tgId}")]
    public IActionResult Get([FromRoute]string tgId)
    {
        var answers = dbContext.UserAnswers.Where(answer => answer.TelegramId == tgId);
        return Ok(answers);
    }
}
