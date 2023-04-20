import unittest
from unittest.mock import MagicMock
from github import Repository
from python.lib.moj_archive import MojArchive


class TestMojArchive(unittest.TestCase):

    def setUp(self) -> None:
        repo_mock = MagicMock(spec=Repository.Repository)
        self.archive = MojArchive(repo_mock)

    def test_archived_property(self):
        self.archive.repo.archived = True
        self.assertEqual(self.archive.archived, True)

    def test_repo_property(self):
        repo_mock = MagicMock(spec=Repository.Repository)
        self.archive._MojArchive__repo = repo_mock
        self.assertEqual(self.archive.repo, repo_mock)

    def test_complete_property(self):
        self.archive.complete = True
        self.assertEqual(self.archive.complete, True)

    def test_allow_list_location_property(self):
        self.archive.allow_list_location = '/usr/local/path/to/allow-list.txt'
        self.assertEqual(self.archive.allow_list_location,
                         '/usr/local/path/to/allow-list.txt')

    def test_allow_list_property(self):
        with unittest.mock.patch('builtins.open',
                                 unittest.mock.mock_open(read_data='repo1\nrepo2\nrepo3\n')):
            self.archive.allow_list_location = '/usr/local/path/to/allow-list.txt'
            allow_list = self.archive.allow_list
        self.assertEqual(allow_list, ['repo1', 'repo2', 'repo3'])

    def test_is_on_allow_list_method(self):
        with unittest.mock.patch('builtins.open',
                                 unittest.mock.mock_open(read_data='repo1\nrepo2\nrepo3\n')):
            self.archive.allow_list_location = '/usr/local/path/to/allow-list.txt'
            repo_mock = MagicMock(spec=Repository.Repository)
            repo_mock.name = 'repo2'
            self.archive._MojArchive__repo = repo_mock
            self.assertEqual(self.archive.is_on_allow_list, True)

    def test_archive_method_returns_true_on_allow_list(self):
        with unittest.mock.patch('builtins.open',
                                 unittest.mock.mock_open(read_data='repo1\nrepo2\nrepo3\n')):
            self.archive.allow_list_location = '/usr/local/path/to/allow-list.txt'
            repo_mock = MagicMock(spec=Repository.Repository)
            repo_mock.name = 'repo2'
            self.archive._MojArchive__repo = repo_mock
            self.assertEqual(self.archive.archive(), True)

    def test_archive_method_returns_true_on_successful_archiving(self):
        with unittest.mock.patch.object(self.archive.repo, 'edit',
                                        return_value=MagicMock(archived=True)):
            self.assertEqual(self.archive.archive(), True)
            self.assertEqual(self.archive.complete, True)

    def test_archive_method_returns_false_on_archiving_failure(self):
        with unittest.mock.patch.object(self.archive.repo, 'edit',
                                        return_value=MagicMock(archived=False)):
            self.assertEqual(self.archive.archive(), True)