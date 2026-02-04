#!/usr/bin/env python3
"""Remove a Discord reminder by job ID."""

import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Remove a Discord reminder")
    parser.add_argument("job_id", help="Job ID to remove")
    
    args = parser.parse_args()
    
    try:
        result = subprocess.run(
            ["openclaw", "cron", "remove", args.job_id],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Removed reminder {args.job_id}")
        else:
            print(f"Error: {result.stderr}", file=sys.stderr)
            sys.exit(1)
            
    except FileNotFoundError:
        print("Error: 'openclaw' CLI not found.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
