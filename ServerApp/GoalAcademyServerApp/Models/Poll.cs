namespace GoalAcademyServerApp.Models;

public class Poll
{
    public Guid Id { get; set; }

    public string PollId { get; set; } = default!;

    public int CorrectOptionId { get; set; }
}