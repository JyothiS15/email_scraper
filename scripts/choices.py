# constants
CONTAINS = "contains"
DOES_NOT_CONTAIN = "does_not_contain"
EQUAL = "equal"
DOES_NOT_EQUAL = "does_not_equal"
LESS_THAN = "less_than"
GREATER_THAN = "greater_than"

# field constants
FROM = "From"
TO = "To"
SUBJECT = "Subject"
DATE = "Date"
STRING = "string"


# label constants
CHAT = "CHAT"
SENT = "SENT"
INBOX = "INBOX"
IMPORTANT = "IMPORTANT"
TRASH = "TRASH"
DRAFT = "DRAFT"
SPAM = "SPAM"
CATEGORY_FORUMS = "CATEGORY_FORUMS"
CATEGORY_UPDATES = "CATEGORY_UPDATES"
CATEGORY_PERSONAL = "CATEGORY_PERSONAL"
CATEGORY_PROMOTIONS = "CATEGORY_PROMOTIONS"
CATEGORY_SOCIAL = "CATEGORY_SOCIAL"
STARRED = "STARRED"
UNREAD = "UNREAD"

# action list
MOVE = "MOVE"
MARK_UNREAD = "MARK_UNREAD"
MARK_READ = "MARK_READ"


# choices
LABELS = [
    INBOX,
    CHAT,
    SENT,
    INBOX,
    IMPORTANT,
    TRASH,
    DRAFT,
    SPAM,
    CATEGORY_FORUMS,
    CATEGORY_UPDATES,
    CATEGORY_PERSONAL,
    CATEGORY_PROMOTIONS,
    CATEGORY_SOCIAL,
    STARRED,
    UNREAD,
]

ACTIONS = [
    MOVE,
    MARK_UNREAD,
    MARK_READ,
]

PREDICATE = {
    CONTAINS: "",
    DOES_NOT_CONTAIN: "-",
    # EQUAL: "e", commenting support for these 2 for now
    # DOES_NOT_EQUAL: "e-",
    LESS_THAN: ">",
    GREATER_THAN: "<",
}


FIELDS = {FROM: "From", TO: "To", SUBJECT: "Subject", DATE: "Date"}
