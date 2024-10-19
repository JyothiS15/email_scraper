# fetch_all_mails and save in DB
import pandas as pd
from dateutil import parser
from db_connection import DBClass
from fetch_emails import GmailMessages


def save_emails():
    gmail_message_object = GmailMessages()

    gmail_message_object.fetch_mails()
    message_response = None
    payloads = []
    print(len(gmail_message_object.message_ids))

    for message_id in gmail_message_object.message_ids:
        message_response = gmail_message_object.get_mail_content(message_id=message_id)
        p = pd.DataFrame(message_response["payload"]["headers"])

        payloads.append(
            {
                "From": p[p["name"] == "From"]["value"].to_list()[0],
                "To": p[p["name"] == "To"]["value"].to_list()[0],
                "Subject": p[p["name"] == "Subject"]["value"].to_list()[0],
                "Date": parser.parse(p[p["name"] == "Date"]["value"].to_list()[0]),
                "id": message_response["id"],
                "ThreadId": message_response["threadId"],
            }
        )

    print(len(payloads))

    db_class = DBClass()
    db_class.write_data(table_name=db_class.MailDump, data=payloads)


if __name__ == "__main__":
    save_emails()
