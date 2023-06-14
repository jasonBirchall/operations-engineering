import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from python.services.sentry_service import UsageStats
from python.services.slack_service import SlackService

START_TIME = "2023-06-08T00:00:00Z"
END_TIME = "2023-06-09T00:00:00Z"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


@patch("slack_sdk.WebClient.__new__")
class TestSlackServiceInit(unittest.TestCase):

    def test_sets_up_class(self, mock_slack_client: MagicMock):
        mock_slack_client.return_value = "test_mock"
        slack_service = SlackService("")
        self.assertEqual("test_mock",
                         slack_service.slack_client)


@patch("slack_sdk.WebClient.__new__")
class TestSlackServiceSendErrorUsageAlertToOperationsEngineering(unittest.TestCase):

    def test_downstream_services_called(self, mock_slack_client: MagicMock):
        SlackService("").send_error_usage_alert_to_operations_engineering(
            0, UsageStats(1, 2, 3, start_time=datetime.strptime(START_TIME,
                                                                DATE_FORMAT),
                          end_time=datetime.strptime(END_TIME,
                                                     DATE_FORMAT)), 4)
        mock_slack_client.return_value.chat_postMessage.assert_called_with(channel='C033QBE511V', mrkdown=True, blocks=[
            {'type': 'section', 'text': {'type': 'mrkdwn',
                                         'text': ':warning: *Sentry Errors Usage Alert :sentry::warning:*\n- Usage threshold: 400%\n- Period: 0 day\n- Max usage for period: 2 Errors\n- Errors consumed over period: 1\n- Percentage consumed: 300%'}},
            {'type': 'divider'}, {'type': 'section', 'text': {'type': 'mrkdwn',
                                                              'text': ' Check Sentry for projects reporting excessive errors :eyes:'},
                                  'accessory': {'type': 'button', 'text': {'type': 'plain_text',
                                                                           'text': ':sentry: Error usage for period',
                                                                           'emoji': True},
                                                'url': 'https://ministryofjustice.sentry.io/stats/?dataCategory=errors&end=2023-06-09T00%3A00%3A00Z&sort=-accepted&start=2023-06-08T00%3A00%3A00Z&utc=true'}}])


@patch("slack_sdk.WebClient.__new__")
class TestSlackServiceSendTransactionUsageAlertToOperationsEngineering(unittest.TestCase):

    def test_downstream_services_called(self, mock_slack_client: MagicMock):
        SlackService("").send_transaction_usage_alert_to_operations_engineering(
            0, UsageStats(1, 2, 3, start_time=datetime.strptime(START_TIME,
                                                                DATE_FORMAT),
                          end_time=datetime.strptime(END_TIME,
                                                     DATE_FORMAT)), 4)
        mock_slack_client.return_value.chat_postMessage.assert_called_with(channel='C033QBE511V', mrkdown=True, blocks=[
            {'type': 'section', 'text': {'type': 'mrkdwn',
                                         'text': ':warning: *Sentry Transactions Usage Alert :sentry::warning:*\n- Usage threshold: 400%\n- Period: 0 day\n- Max usage for period: 2 Transactions\n- Transactions consumed over period: 1\n- Percentage consumed: 300%'}},
            {'type': 'divider'}, {'type': 'section', 'text': {'type': 'mrkdwn',
                                                              'text': ' Check Sentry for projects consuming excessive transactions :eyes:'},
                                  'accessory': {'type': 'button', 'text': {'type': 'plain_text',
                                                                           'text': ':sentry: Transaction usage for period',
                                                                           'emoji': True},
                                                'url': 'https://ministryofjustice.sentry.io/stats/?dataCategory=transactions&end=2023-06-09T00%3A00%3A00Z&sort=-accepted&start=2023-06-08T00%3A00%3A00Z&utc=true'}}])


if __name__ == "__main__":
    unittest.main()