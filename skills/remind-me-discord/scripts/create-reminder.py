#!/usr/bin/env python3
"""
Create a Discord reminder.
Usage: python create-reminder.py "提醒内容" "时间描述" [--channel CHANNEL_ID]
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta
import re

# Default Discord channel (should be configured per user)
DEFAULT_CHANNEL = "1468182064514728000"

# Workspace path
WORKSPACE = r"C:\Users\Asus\.openclaw\workspace"
LOG_FILE = f"{WORKSPACE}\
eminders-discord.md"


def parse_time(time_str):
    """Parse natural language time to timestamp."""
    time_str = time_str.lower().strip()
    now = datetime.now()
    
    # "in X minutes/hours/days"
    if time_str.startswith("in "):
        match = re.match(r'in (\d+) (minute|minutes|hour|hours|day|days)', time_str)
        if match:
            num = int(match.group(1))
            unit = match.group(2)
            if unit.startswith('minute'):
                return now + timedelta(minutes=num)
            elif unit.startswith('hour'):
                return now + timedelta(hours=num)
            elif unit.startswith('day'):
                return now + timedelta(days=num)
    
    # "today at HH:MM"
    if time_str.startswith("today at "):
        time_part = time_str[9:].strip()
        try:
            hour, minute = map(int, time_part.split(':'))
            return now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        except:
            pass
    
    # "tomorrow at HH:MM"
    if time_str.startswith("tomorrow at "):
        time_part = time_str[12:].strip()
        try:
            hour, minute = map(int, time_part.split(':'))
            tomorrow = now + timedelta(days=1)
            return tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
        except:
            pass
    
    # ISO format "YYYY-MM-DD HH:MM"
    try:
        return datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    except:
        pass
    
    # Try time only "HH:MM"
    try:
        hour, minute = map(int, time_str.split(':'))
        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if target < now:
            target += timedelta(days=1)
        return target
    except:
        pass
    
    return None


def find_openclaw_cli():
    """Find openclaw CLI executable."""
    import shutil
    
    # Try common locations
    possible_paths = [
        "openclaw",
        r"C:\Users\Asus\AppData\Roaming\npm\openclaw.cmd",
        r"C:\Users\Asus\AppData\Roaming\npm\openclaw",
        r"D:\desktop\openclaw\node_modules\.bin\openclaw.cmd",
    ]
    
    for path in possible_paths:
        if shutil.which(path):
            return path
    
    # Check npm prefix
    try:
        result = subprocess.run(["npm", "prefix", "-g"], capture_output=True, text=True)
        if result.returncode == 0:
            npm_prefix = result.stdout.strip()
            cli_path = f"{npm_prefix}\\openclaw.cmd"
            if shutil.which(cli_path):
                return cli_path
    except:
        pass
    
    return None


def create_cron_job(text, at_ms, channel, recurring=False):
    """Create a cron job using openclaw CLI."""
    
    # Find openclaw CLI
    openclaw_cli = find_openclaw_cli()
    if not openclaw_cli:
        print("Error: 'openclaw' CLI not found. Trying direct tool call...", file=sys.stderr)
        # Fall back to telling user to use the cron tool directly
        return create_via_fallback(text, at_ms, channel)
    
    # Build the message that will be sent
    message_content = f"⏰ 提醒：{text}"
    
    # The agentTurn message instructs the agent to call the message tool
    agent_message = f"""请调用 message 工具发送以下消息到 Discord channel {channel}：

{message_content}

请回复 NO_REPLY 不要重复发送。"""
    
    job = {
        "name": f"Discord提醒: {text[:20]}",
        "enabled": True,
        "schedule": {
            "kind": "at",
            "atMs": int(at_ms)
        },
        "sessionTarget": "isolated",
        "wakeMode": "next-heartbeat",
        "payload": {
            "kind": "agentTurn",
            "message": agent_message
        }
    }
    
    # Use openclaw cron add command
    job_json = json.dumps(job, ensure_ascii=False)
    
    try:
        result = subprocess.run(
            [openclaw_cli, "cron", "add"],
            input=job_json,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            print(f"Error creating cron job: {result.stderr}", file=sys.stderr)
            return None
        
        # Parse response to get job ID
        try:
            response = json.loads(result.stdout)
            return response.get("id")
        except:
            # Try to extract ID from output
            match = re.search(r'"id":\s*"([^"]+)"', result.stdout)
            if match:
                return match.group(1)
            return "unknown"
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


def create_via_fallback(text, at_ms, channel):
    """Fallback: output job JSON for manual creation."""
    print("⚠️  Could not find openclaw CLI automatically.")
    print("\nPlease use the cron tool directly with this job definition:\n")
    
    message_content = f"⏰ 提醒：{text}"
    agent_message = f"""请调用 message 工具发送以下消息到 Discord channel {channel}：

{message_content}

请回复 NO_REPLY 不要重复发送。"""
    
    job = {
        "name": f"Discord提醒: {text[:20]}",
        "enabled": True,
        "schedule": {
            "kind": "at",
            "atMs": int(at_ms)
        },
        "sessionTarget": "isolated",
        "wakeMode": "next-heartbeat",
        "payload": {
            "kind": "agentTurn",
            "message": agent_message
        }
    }
    
    print(json.dumps(job, ensure_ascii=False, indent=2))
    print("\nOr ask your AI assistant to create this cron job for you!")
    return None


def log_reminder(text, time_str, job_id, target_time):
    """Log the reminder to markdown file."""
    timestamp = target_time.strftime("%Y-%m-%d %H:%M")
    log_entry = f"- [pending] {timestamp} | {text} (id: {job_id})\n"
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except:
        pass  # Log failure is not critical


def main():
    parser = argparse.ArgumentParser(description="Create a Discord reminder")
    parser.add_argument("text", help="Reminder text")
    parser.add_argument("time", help="Time description (e.g., 'in 30 minutes', 'today at 14:30')")
    parser.add_argument("--channel", default=DEFAULT_CHANNEL, help="Discord channel ID")
    
    args = parser.parse_args()
    
    # Parse time
    target_time = parse_time(args.time)
    if not target_time:
        print(f"Error: Could not parse time '{args.time}'", file=sys.stderr)
        print("Supported formats: 'in X minutes/hours/days', 'today at HH:MM', 'tomorrow at HH:MM', 'YYYY-MM-DD HH:MM'", file=sys.stderr)
        sys.exit(1)
    
    if target_time < datetime.now():
        print(f"Error: Time {target_time} is in the past", file=sys.stderr)
        sys.exit(1)
    
    # Convert to milliseconds timestamp
    at_ms = target_time.timestamp() * 1000
    
    # Create cron job
    job_id = create_cron_job(args.text, at_ms, args.channel)
    if not job_id:
        sys.exit(1)
    
    # Log reminder
    log_reminder(args.text, args.time, job_id, target_time)
    
    # Output success
    print(f"✅ Reminder set!")
    print(f"   Content: {args.text}")
    print(f"   Time: {target_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"   Job ID: {job_id}")


if __name__ == "__main__":
    main()
