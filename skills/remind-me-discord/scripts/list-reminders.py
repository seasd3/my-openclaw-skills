#!/usr/bin/env python3
"""List pending Discord reminders."""

import subprocess
import json


def main():
    try:
        result = subprocess.run(
            ["openclaw", "cron", "list"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return
        
        jobs = json.loads(result.stdout)
        
        # Filter for Discord reminders
        discord_jobs = [
            j for j in jobs 
            if j.get("sessionTarget") == "isolated" and 
            j.get("payload", {}).get("kind") == "agentTurn"
        ]
        
        if not discord_jobs:
            print("No pending Discord reminders.")
            return
        
        print(f"Pending Discord reminders ({len(discord_jobs)}):\n")
        
        for job in discord_jobs:
            job_id = job.get("id", "unknown")[:8]
            name = job.get("name", "Untitled")
            schedule = job.get("schedule", {})
            enabled = "✅" if job.get("enabled") else "❌"
            
            if schedule.get("kind") == "at":
                from datetime import datetime
                at_ms = schedule.get("atMs", 0)
                time_str = datetime.fromtimestamp(at_ms / 1000).strftime("%Y-%m-%d %H:%M")
                print(f"{enabled} [{job_id}...] {time_str} | {name}")
            else:
                print(f"{enabled} [{job_id}...] {schedule} | {name}")
                
    except FileNotFoundError:
        print("Error: 'openclaw' CLI not found.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
