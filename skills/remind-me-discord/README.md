# Discord Remind Me

Set reminders that actively send messages to Discord. Unlike the basic remind-me skill, this one actually delivers messages to your Discord channel!

## Features

- ⏰ Natural language time parsing
- 📨 Direct Discord message delivery
- 🔄 One-time or recurring reminders
- 📝 Simple markdown-based reminder log

## Usage

### Set a reminder

```bash
# Basic
bash ./scripts/create-reminder.sh "开会" "in 30 minutes"

# Specific time
bash ./scripts/create-reminder.sh "吃饭" "today at 12:30"

# Recurring daily
bash ./scripts/create-reminder.sh "打卡" "every day at 9am"

# Recurring weekly
bash ./scripts/create-reminder.sh "周会" "every Monday at 10am"
```

### List reminders

```bash
bash ./scripts/list-reminders.sh
```

### Remove a reminder

```bash
bash ./scripts/remove-reminder.sh <job-id>
```

## How It Works

1. Parses natural language time (e.g., "in 30 minutes")
2. Creates a cron job with `sessionTarget: "isolated"`
3. At the scheduled time, spawns an agent to send the message
4. Message is delivered via Discord channel

## Time Formats

**One-time:**
- "in 5 minutes"
- "in 2 hours"
- "tomorrow at 9am"
- "today at 15:30"
- "2026-02-05 14:00"

**Recurring:**
- "every 30 minutes"
- "every hour"
- "every day at 9am"
- "every Monday at 10am"
- "weekly at 2pm"

## Log

Reminders are logged to `reminders-discord.md`:
```markdown
- [pending] 2026-02-04 10:30 | 开会 (id: abc-123)
- [sent] 2026-02-04 09:00 | 吃早饭 (id: def-456)
```
