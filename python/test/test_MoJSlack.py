import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta

from python.lib.moj_slack import MojSlack


class MojSlackTestCase(unittest.TestCase):
    def setUp(self):
        self.slack_token = "test_token"
        self.slack_client = MagicMock()
        self.slack = MojSlack(self.slack_token)
        self.slack.client = self.slack_client

    def test_get_conversation_history(self):
        channel_id = "test_casdasasdhannel_id"
        days = 7

        mock_response_1 = {
            "messages": [{"ts": datetime.timestamp(datetime.now())}],
            "has_more": True,
            "response_metadata": {"next_cursor": "test_cursor_1"},
        }

        mock_response_2 = {
            "messages": [{"ts": datetime.timestamp(datetime.now())}],
            "has_more": False,
        }

        self.slack_client.conversations_history.side_effect = [
            mock_response_1,
            mock_response_2,
        ]

        messages = self.slack.get_conversation_history(channel_id, days)

        self.assertEqual(len(messages), 2)

    def test_generate_datetime(self):
        number_of_days = 7
        expected_date = (datetime.now() -
                         timedelta(number_of_days)).timestamp()

        actual_date = self.slack.generate_datetime(number_of_days)

        self.assertEqual(int(actual_date), int(expected_date))

    def test_filter_out_subtypes(self):
        message1 = {"text": "test message"}
        message2 = {
            "text": "test bot measdasdssage",
            "subtype": "bot_masdasdessage",
        }
        message3 = {
            "text": "test channel message",
            "subtype": "channel_join",
        }

        messages = [message1, message2, message3]

        filtered_messages = self.slack.filter_out_subtypes(messages)

        self.assertEqual(len(filtered_messages), 1)
        self.assertEqual(filtered_messages[0], message1)


if __name__ == "__main__":
    unittest.main()
