---
name: remind-me-discord
description: Set reminders that actively send messages to Discord at scheduled times. Unlike basic reminders, these actually deliver to your Discord channel!
metadata:
  emoji: ⏰
  requires:
    bins: ["openclaw", "python"]
---

# Discord Remind Me

Active reminders for Discord. No more "I forgot to check" — messages come to you!

## How It Works

```
You: "5分钟后提醒我开会"
  ↓
Cron job created (isolated session)
  ↓
⏰ Time's up!
  ↓
Agent spawns → calls message tool → Discord notification
```

## Usage

### Quick Set

```bash
# In 30 minutes
python C:\Users\Asus\.openclaw\workspace\skills\remind-me-discord\scripts\create-reminder.py "开会" "in 30 minutes"

# Today at 2:30 PM
python ...\create-reminder.py "吃饭" "today at 14:30"

# Tomorrow morning
python ...\create-reminder.py "早起" "tomorrow at 8:00"
```

### List Pending

```bash
python ...\list-reminders.py
```

### Remove

```bash
python ...\remove-reminder.py <job-id>
```

## Time Formats

| Format | Example |
|--------|---------|
| In X minutes | `in 5 minutes` |
| In X hours | `in 2 hours` |
| Today at | `today at 14:30` |
| Tomorrow at | `tomorrow at 9:00` |
| Absolute | `2026-02-05 15:30` |

## Key Differences from Basic remind-me

| Feature | Basic remind-me | Discord Remind Me |
|---------|-----------------|-------------------|
| Delivery | System event (passive) | Discord message (active) |
| Session | main | isolated |
| Visibility | In-chat only | Channel notification |
| Reliability | Depends on heartbeat | Guaranteed delivery |

## Configuration

Edit the script to change default channel:

```python
# create-reminder.py
DEFAULT_CHANNEL = "1468182064514728000"  # Change to your channel
```

## Log

All reminders logged to `reminders-discord.md`:

```markdown
- [pending] 2026-02-04 10:30 | 开会 (id: abc-123)
- [sent] 2026-02-04 09:00 | 吃早饭 (id: def-456)
```

## Troubleshooting

**Job not triggering?**
- Check `enabled: true` is set
- Verify `openclaw cron list` shows the job
- Check `nextWakeAtMs` is not null

**Message not delivered?**
- Verify channel ID is correct
- Check Discord bot has send permissions
- Look at job run logs: `openclaw cron runs <job-id>`
