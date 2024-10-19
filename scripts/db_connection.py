import os
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    String,
    and_,
    create_engine,
    insert,
    or_,
    select,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class DBClass:
    # Define Table Classes
    Base = declarative_base()

    class MailDump(Base):
        __tablename__ = "mail_dump"

        id = Column(String(length=40), primary_key=True)
        From = Column(String(length=100))
        To = Column(String(length=100))
        Subject = Column(String(length=100))
        Date = Column(DateTime)
        ThreadId = Column(String(length=20))
        Presence = Column(Boolean, default=True)

    def __init__(self) -> None:
        self.engine = create_engine(os.environ.get(
            "DB_URL",
            "postgresql+psycopg2://postgres:1234\
@localhost/gmail_hub")
                                    )

    def create_table(self):
        """
        run only the first time
        table name and fields
        Emails -
            1. From
            2. To
            3. Subject
            4. Date
            5. id
            6. ThreadId
            7. Presence
        """

        # Create the tables in the database
        self.Base.metadata.create_all(self.engine)

    def write_data(self, table_name, data):

        # check ids if already exists
        ids = [d['id'] for d in data]
        stmt = select(table_name.id).where(table_name.id.in_(ids))
        with self.engine.connect() as conn:
            exisitng_data = conn.execute(stmt)
            conn.commit()

        # maintaining the ids thats already present so that it can be skiped
        exisitng_ids = []
        for d in exisitng_data:
            exisitng_ids.append(d.id)

        # create a new payload with no ids present from the existing ones.
        final_data = []
        for d in data:
            if d["id"] not in exisitng_ids:
                final_data.append(d)
        print("data to be inserted is")
        print(final_data)
        if not final_data:
            return
        insert_statement = insert(table_name).values(final_data)

        with self.engine.connect() as conn:
            _ = conn.execute(insert_statement)
            conn.commit()

    def read_data(self, kwargs, rule="AND"):
        session = sessionmaker(bind=self.engine)()
        filters = []
        for column, value in kwargs.items():
            if "Date" in column:
                if "<" in column:
                    filters.append(self.MailDump.Date < value)
                else:
                    filters.append(self.MailDump.Date > value)
                continue

            if not isinstance(value, list):
                if value[0] == "-":
                    filters.append(
                        ~getattr(self.MailDump, column).like(f"%{value[1:]}%")
                    )
                else:
                    filters.append(getattr(self.MailDump, column).like(f"%{value}%"))
            else:
                temp = []
                for val in value:
                    if val[0] == "-":
                        temp.append(
                            ~getattr(self.MailDump, column).like(f"%{val[1:]}%")
                        )
                    else:
                        temp.append(getattr(self.MailDump, column).like(f"%{val}%"))
                filters.append(or_(*temp))
        if rule == "OR":
            filters = or_(*filters)
        elif rule == "AND":
            filters = and_(*filters)
        else:
            raise Exception(f"Rule not supported {rule}")
        query_set = session.query(self.MailDump).filter(filters).all()

        return query_set


if __name__ == "__main__":
    db_class = DBClass()
    db_class.create_table()
    # values = db_class.read_data(rule="OR", kwargs={"From": "uber"})
    # for i in values:
    #     print(i.id)
