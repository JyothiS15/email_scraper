# Email Scraper Python Project

## Objective
The Project helps with connecting to any gmail account, fetching mails, dumping them into a DB based on requirements, and using the same data for running actions on the mails based on set of rules

## Setup

1. create a virtual environment
```
python manage.py -m venv venv
```
3. install all the requirements
```
pip install -r requirements.txt
```
4. run migration files
```
python email_scraper\scripts\db_connection.py # run mainly the create_db function of the class.
```
5. Download credentials.json file from Gmail API and SERVICES
```
Follow the steps at https://developers.google.com/gmail/api/quickstart/python
```
6. run script to save mails into the tables created in the DB.
```
python email_scraper\scripts\fetch_emails.py # Have set limit of 16 mails for now, you can increase the count or uncomment the portion of code to sync all mails in first go. IMPORTANT - If ran the same script again on same mails, possible that insert command might not insert any mails because they are already present in the db table.
```
7. run script to run actions
```
python email_scraper\scripts\actions_on_email.py # Run this file with any rule you might want and it gets applied. The choices.py file has list of actions, conditions i support currently.
```
8. run fast api to expose 6th feature via api
```
fastapi dev .\scripts\endpoint.py # Spins up a fast api server, which mimics 6th action with payload you pass in the payload.
```
9. example of the payload
```
curl --location 'http://127.0.0.1:8000/' \
--header 'Content-Type: application/json' \
--data '{
    "predict": {
        "conditions": [
            {
                "Field": "From",
                "predicte": "contains",
                "value": "uber"
            },
            {
                "Field": "Subject",
                "predicte": "contains",
                "value": "Jyothi"
            },
            {
                "Field": "Date",
                "predicte": "less_than",
                "value": "10"
            }
        ],
        "rule": "AND"
    },
    "action": {
        "MARK_READ": "None",
        "MOVE": [
            "STARRED"
        ]
    }
}'
```
