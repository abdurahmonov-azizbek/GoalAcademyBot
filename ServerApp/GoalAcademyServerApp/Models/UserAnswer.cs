namespace GoalAcademyServerApp.Models;

public class UserAnswer
{
    public Guid Id { get; set; }

    public string PollId { get; set; } = default!;

    public int OptionId { get; set; }

    public string TelegramId { get; set; } = default!;
}
