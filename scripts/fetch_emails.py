from email_utils import GmailConnector
from googleapiclient.errors import HttpError


class GmailMessages(GmailConnector):
    def __init__(self):
        super().__init__()

    def fetch_mails(self):
        try:
            all_messages = []
            messages = (
                self.service.users()
                .messages()
                .list(userId="me", labelIds=["INBOX"], maxResults=16)
                .execute()
            )
            # print(messages)
            print(len(messages["messages"]))
            all_messages.extend(messages["messages"])
            # while messages.get('nextPageToken'):

            #     messages = self.service.users().messages().list(
            #         userId="me",
            #         labelIds=["INBOX"],
            #         maxResults=500,
            #         pageToken=messages['nextPageToken']).execute()
            #     print(len(messages['messages']))
            #     all_messages.extend(messages['messages'])

            self.message_ids = [i["id"] for i in all_messages]

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")

    def fetch_mail(self, message_id: str):
        try:
            return (
                self.service.users()
                .messages()
                .get(
                    userId="me",
                    id=message_id,
                )
                .execute()["id"]
            )
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")
            return None

    def get_mail_content(self, message_id, number=2):
        try:
            return (
                self.service.users()
                .messages()
                .get(userId="me", id=message_id, format="full")
                .execute()
            )

        except Exception as error:
            print(f"An error occurred: {error}")


if __name__ == "__main__":
    gm_object = GmailMessages()
    response = gm_object.get_mail_content("19252ea5944a5cfe")
