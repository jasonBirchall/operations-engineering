from services.github_service import GithubService
from services.auth0_service import Auth0Service
import sys

DORMANT_USER_THRESHOLD = 90


def setup_environment() -> tuple[str, str]:

    github_token = sys.argv[0]
    auth0_client_secret = sys.argv[1]
    auth0_client_id = sys.argv[2]
    auth0_domain = sys.argv[3]

    return github_token, auth0_client_secret, auth0_client_id, auth0_domain


def get_audit_logs(auth0_service: Auth0Service) -> list[str]:

    active_users =[ user["user_id"] for user in auth0_service.get_active_users() ]

    return active_users


def identify_dormant_users(github_users: list[str], audit_logs: list[str]) -> list[str]:
    return [ user for user in github_users if user not in audit_logs ]


def identify_dormant_github_users():
    github_token, auth0_client_secret, auth0_client_id, auth0_domain = setup_environment()

    github = GithubService(github_token, "ministryofjustice")
    auth0_service = Auth0Service(auth0_client_secret, auth0_client_id, auth0_domain, "client_credentials")

    active_users = get_audit_logs(github, auth0_service)
    all_users = github.get_users_of_multiple_organisations(["ministryofjustice", "moj-analytical-services"])

    dormant_users = identify_dormant_users(all_users, active_users)

    for user in dormant_users:
        print(user)


if __name__ == "__main__":
    identify_dormant_github_users()