from pathlib import Path
from datetime import datetime


# Find project folder
project_folder = Path(__file__).resolve().parent.parent

# Create results folder
results_folder = project_folder / "results"
results_folder.mkdir(exist_ok=True)

# Alert log file
alert_file = results_folder / "alerts.log"


def send_alert(login_data, risk_score):
    """
    Save high-risk login activity into an alert log.
    """

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    alert_message = (
        f"\n[{current_time}] BRUTE-FORCE ALERT\n"
        f"Risk Score: {risk_score:.2f}%\n"
        f"Login Data: {login_data}\n"
        f"{'-' * 50}\n"
    )

    with open(alert_file, "a", encoding="utf-8") as file:
        file.write(alert_message)

    print("🚨 Alert saved to alerts.log")


if __name__ == "__main__":

    sample_login_data = {
        "login_attempts": 80,
        "failed_attempts": 60,
        "time_between_attempts": 0.5,
        "unique_usernames": 20,
        "ip_reputation": 0.1
    }

    sample_risk_score = 92.5

    send_alert(
        sample_login_data,
        sample_risk_score
    )