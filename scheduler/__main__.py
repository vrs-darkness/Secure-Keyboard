import subprocess
import os
import sys
from datetime import datetime

CRON_JOB_COMMENT = "# Scheduled Python Job"


def start():
    """Schedules a cron job that sources the virtual environment."""
    start_time = datetime.now()
    project_root = os.path.abspath(os.path.dirname(__file__) + "/..")
    venv_path = os.path.abspath(".venv/bin/python3")

    cron_schedule = os.getenv("CRON_SCHEDULE", "* * * * *")
    log_file = os.path.abspath("./cron.log")

    # Cron job command: source venv, set PYTHONPATH, and run the script
    cron_command = f'(crontab -l 2>/dev/null; echo "{cron_schedule} PYTHONPATH={project_root} {venv_path} -m scheduler.schedule.periodic_task >> {log_file} 2>&1 {CRON_JOB_COMMENT}") | crontab -' # noqa

    subprocess.run(cron_command, shell=True, check=True)
    print(f"Cron job scheduled with: {cron_schedule}")
    print(f"Cron job started at: {start_time}")


def stop():
    """Removes the scheduled cron job."""
    cron_command = f'crontab -l | grep -v "{CRON_JOB_COMMENT}" | crontab -'
    subprocess.run(cron_command, shell=True, check=True)
    print("Cron job stopped.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "start":
        start()
    else:
        if len(sys.argv) > 1 and sys.argv[1] == "stop":
            stop()
        else:
            print("Usage: python3 -m scheduler start / stop")
