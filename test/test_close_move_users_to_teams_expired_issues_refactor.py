from dataclasses import dataclass
import unittest
from unittest.mock import patch, MagicMock

from bin.close_move_users_to_teams_expired_issues_refactor import (
    close_expired_move_users_to_teams_issues,
    main
)


@dataclass
class Repository:
    name: str = ""


class TestCloseExpiredMoveUsersToTeamsIssues(unittest.TestCase):
    @patch("bin.close_move_users_to_teams_expired_issues_refactor.GithubService", new=MagicMock)
    @patch("bin.close_move_users_to_teams_expired_issues_refactor.get_org_repositories")
    @patch("bin.close_move_users_to_teams_expired_issues_refactor.get_environment_variables")
    def test_main(self, mock_get_environment_variables, mock_get_org_repositories):
        mock_get_environment_variables.return_value = "", ""
        mock_get_org_repositories.return_value = MagicMock()
        main()
        mock_get_org_repositories.assert_called()
        mock_get_environment_variables.assert_called()

    @patch("bin.close_move_users_to_teams_expired_issues_refactor.get_org_repositories")
    @patch("services.github_service.GithubService")
    def test_closed_expired_issues_when_repo_exists(self, mock_github_service, mock_get_org_repositories):
        mock_get_org_repositories.return_value = [Repository("some-repo")]
        close_expired_move_users_to_teams_issues(
            mock_github_service, "some-org")
        mock_github_service.close_expired_issues.assert_called()

    @patch("bin.close_move_users_to_teams_expired_issues_refactor.get_org_repositories")
    @patch("services.github_service.GithubService")
    def test_closed_expired_issues_when_no_repo_exists(self, mock_github_service, mock_get_org_repositories):
        mock_get_org_repositories.return_value = []
        close_expired_move_users_to_teams_issues(
            mock_github_service, "some-org")
        mock_github_service.close_expired_issues.assert_not_called()


if __name__ == "__main__":
    unittest.main()