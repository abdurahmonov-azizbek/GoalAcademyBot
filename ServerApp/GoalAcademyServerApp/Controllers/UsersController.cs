using GoalAcademyServerApp.DbContexts;
using GoalAcademyServerApp.Models;
using Microsoft.AspNetCore.Mvc;

namespace GoalAcademyServerApp.Controllers;

[ApiController]
[Route("api/[controller]")]
public class UsersController(AppDbContext dbContext) : ControllerBase
{
    [HttpPost]
    public IActionResult Create([FromBody] UserDto userDto)
    {
        var user = new User
        {
            Id = Guid.NewGuid(),
            TelegramId = userDto.TelegramId
        };

        dbContext.Users.Add(user);  
        dbContext.SaveChanges();
        return Ok(user);
    }

    [HttpGet("exist/{telegramId}")]
    public IActionResult UserExists([FromRoute] string telegramId)
    {
        var user = dbContext.Users.FirstOrDefault(user => user.TelegramId == telegramId);

        return Ok(user is not null);
    }

    [HttpGet("result/{tgId}")]
    public IActionResult GetResult([FromRoute] string tgId)
    {
        var polls = dbContext.Polls.ToList();
        var userAnswers = dbContext.UserAnswers.Where(answer => answer.TelegramId == tgId).ToList();
        var blns = new List<bool>();

        foreach(var answer in userAnswers)
        {
            var poll = polls.FirstOrDefault(poll => poll.PollId == answer.PollId);
            
            if (poll is null)
                continue;

            blns.Add(answer.OptionId == poll.CorrectOptionId);
        }

        return Ok(blns.Count(b => b == true));

    }
}

public class UserDto
{
    public string TelegramId { get; set; } = default!;
}
