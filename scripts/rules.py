from choices import (
    CONTAINS,
    DATE,
    FIELDS,
    FROM,
    GREATER_THAN,
    INBOX,
    LESS_THAN,
    MARK_READ,
    MARK_UNREAD,
    MOVE,
    PREDICATE,
    SUBJECT,
)

rules = [
    {
        "predict": {
            "conditions": [
                {
                    "Field": FIELDS[FROM],
                    "predicte": PREDICATE[CONTAINS],
                    "value": "tenmiles.com",
                },
                {
                    "Field": FIELDS[SUBJECT],
                    "predicte": PREDICATE[CONTAINS],
                    "value": "Interview",
                },
                {
                    "Field": FIELDS[DATE],
                    "predicte": PREDICATE[LESS_THAN],
                    "value": "2",
                },
            ],
            "rule": "OR",
        },
        "action": {
            MARK_READ: None,
            MOVE: [INBOX],
        },
    },
    {
        "predict": {
            "conditions": [
                {
                    "Field": FIELDS[FROM],
                    "predicte": PREDICATE[CONTAINS],
                    "value": "jyothi.s1798@gmail.com",
                },
                {
                    "Field": FIELDS[DATE],
                    "predicte": PREDICATE[GREATER_THAN],
                    "value": "2",
                },
            ],
            "rule": "AND",
        },
        "action": {
            MARK_UNREAD: None,
            MOVE: ["NEW_LABEL"],
        },
    },
]
