using GoalAcademyServerApp.Models;
using Microsoft.EntityFrameworkCore;

namespace GoalAcademyServerApp.DbContexts;

public class AppDbContext : DbContext
{
    public DbSet<User> Users => Set<User>();

    public DbSet<Poll> Polls => Set<Poll>();

    public DbSet<UserAnswer> UserAnswers => Set<UserAnswer>();

    public AppDbContext(DbContextOptions options) : base(options)
    {
    }
}
