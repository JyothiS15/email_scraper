from datetime import datetime, timedelta
from typing import Dict, List

import pandas as pd
from choices import (
    ACTIONS,
    CONTAINS,
    DATE,
    FIELDS,
    FROM,
    LESS_THAN,
    MARK_READ,
    MARK_UNREAD,
    MOVE,
    SUBJECT,
    PREDICATE
)
from db_connection import DBClass
from fetch_emails import GmailMessages
from googleapiclient.errors import HttpError


class GmailMessagesActions(GmailMessages):
    def __init__(self):
        super().__init__()

    def _validate_actions(self, actions: str):
        for action in actions:
            if action not in ACTIONS:
                raise Exception(f"{action} is not supported")

    def _validate_labels(self, labels: List[str]):
        valid_labels = self.service.users().labels().list(userId="me").execute()
        valid_labels = pd.DataFrame(valid_labels["labels"])["name"].to_list()

        accepted_labels = set(labels).intersection(set(valid_labels))

        return list(accepted_labels)

    def mark_them_read(self, message_ids: List[str]):
        try:
            # validate the message ids
            messages = [self.fetch_mail(message_id=m) for m in message_ids]
            valid_message_ids = set(messages).intersection(set(message_ids))
            query = {"removeLabelIds": ["UNREAD"]}
            for valid_message_id in valid_message_ids:
                print(f"read the mail {valid_message_id}")
                self.service.users().messages().modify(
                    userId="me", id=valid_message_id, body=query
                ).execute()

        except HttpError as error:
            print(f"An error occurred: {error}")
            raise Exception(error)

    def mark_them_unread(self, message_ids: List[str]):
        try:
            # validate the message ids
            messages = [self.fetch_mail(message_id=m) for m in message_ids]
            valid_message_ids = set(messages).intersection(set(message_ids))
            query = {"addLabelIds": ["UNREAD"]}
            for valid_message_id in valid_message_ids:
                self.service.users().messages().modify(
                    userId="me", id=valid_message_id, body=query
                ).execute()

        except HttpError as error:
            print(f"An error occurred: {error}")
            raise Exception(error)

    def move_to_folders(self, message_ids: List[str], labels):
        try:
            labels = self._validate_labels(labels=labels)
            messages = [self.fetch_mail(message_id=m) for m in message_ids]
            valid_message_ids = set(messages).intersection(set(message_ids))

            query = {"addLabelIds": labels}

            for valid_message_id in valid_message_ids:
                self.service.users().messages().modify(
                    userId="me", id=valid_message_id, body=query
                ).execute()

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")

    def take_actions(self, rules: Dict):
        predicates = rules["predict"]
        actions = rules["action"]

        # create payload for db fetch
        kwargs = {}
        for i in predicates["conditions"]:
            if i["Field"] == DATE:
                kwargs[i["Field"] + i["predicte"]] = datetime.now() - timedelta(
                    days=int(i["value"])
                )
            else:
                kwargs[i["Field"]] = i["predicte"] + i["value"]

        # fetch all valid message ids from DB
        db_class = DBClass()
        messages = db_class.read_data(rule=predicates["rule"], kwargs=kwargs)
        valid_message_ids = []
        for i in messages:
            valid_message_ids.append(i.id)

        self._validate_actions(actions=actions.keys())

        for action, payload in actions.items():
            print(action)
            if action == MARK_READ:
                self.mark_them_read(message_ids=valid_message_ids)
            elif action == MARK_UNREAD:
                self.mark_them_unread(message_ids=valid_message_ids)
            else:
                self.move_to_folders(message_ids=valid_message_ids, labels=payload)


if __name__ == "__main__":
    g = GmailMessagesActions()
    rules = {
        "predict": {
            "conditions": [
                {
                    "Field": FIELDS[FROM],
                    "predicte": PREDICATE[CONTAINS],
                    "value": "uber",
                },
                {
                    "Field": FIELDS[SUBJECT],
                    "predicte": PREDICATE[CONTAINS],
                    "value": "Jyothi",
                },
                {
                    "Field": FIELDS[DATE],
                    "predicte": PREDICATE[LESS_THAN],
                    "value": 10,
                },
            ],
            "rule": "AND",
        },
        "action": {
            MARK_READ: None,
            MOVE: ["STARRED"],
        },
    }
    print(rules)
    print("------------------")
    g.take_actions(rules=rules)
