import os
from datetime import datetime, timedelta
from config.constants import MINISTRY_OF_JUSTICE, SLACK_CHANNEL, OPERATIONS_ENGINEERING_GITHUB_USERNAMES

from services.github_service import GithubService
from services.slack_service import SlackService

def get_environment_variables() -> tuple:
    slack_token = os.getenv("ADMIN_SLACK_TOKEN")
    if not slack_token:
        raise ValueError(
            "The env variable ADMIN_SLACK_TOKEN is empty or missing")
    github_token = os.getenv("ADMIN_GITHUB_TOKEN")
    if not github_token:
        raise ValueError(
            "The env variable ADMIN_GITHUB_TOKEN is empty or missing")

    return slack_token, github_token


def _calculate_date(in_last_days: int) -> str:
    current_date = datetime.now()
    date = current_date - timedelta(days=in_last_days)
    timestamp_format = "%Y-%m-%d"
    return date.strftime(timestamp_format)

def new_members_detected_message(new_members_added_by_oe, new_members_added_externally, percentage, total_new_members, org, audit_log_url, time_delta_in_days):
    msg = (
        f"Hi all, \n\n"
        f"Here are the {total_new_members} new joiners added in the last {time_delta_in_days} days within the '{org}' GitHub org. \n\n"
        f"*Added by Operations Engineering:*\n"
        f"{new_members_added_by_oe}\n\n"
        f"*Added externally:*\n"
        f"{new_members_added_externally}\n\n"
        f"{percentage}% of the new joiners were added by operations engineering.\n\n"
        f"Please review the audit log for more details: {audit_log_url}\n\n"
        f"Have a swell day, \n\n"
        "The GitHub Organisation Monitoring Bot"
    )

    return msg

def main():
    audit_log_url = f"https://github.com/organizations/{MINISTRY_OF_JUSTICE}/settings/audit-log?q=action%3Aorg.add_member"

    time_delta_in_days = 7
    slack_token, github_token = get_environment_variables()

    github_service = GithubService(str(github_token), MINISTRY_OF_JUSTICE)
    slack_service = SlackService(str(slack_token))
    
    new_members = github_service.check_for_audit_log_new_members(_calculate_date(time_delta_in_days))
    new_members_added_by_oe = ""
    new_members_added_externally = ""
    total_members_added_by_oe = 0
    total_new_members = len(new_members)


    if new_members:
        for member in new_members:
            individual_message = f"{member['userLogin']} added by {member['actorLogin']}.\n"
            if member['actorLogin'] in OPERATIONS_ENGINEERING_GITHUB_USERNAMES:
                new_members_added_by_oe += individual_message
                total_members_added_by_oe += 1
            else:
                new_members_added_externally += individual_message
                
        percentage = round((total_members_added_by_oe / len(new_members)) * 100)

        slack_service.send_message_to_plaintext_channel_name(
            new_members_detected_message("new members from ops eng", "new external members", percentage, total_new_members, MINISTRY_OF_JUSTICE, audit_log_url, time_delta_in_days), SLACK_CHANNEL)


if __name__ == "__main__":
    main()

