from datetime import datetime

from dotenv import load_dotenv
from typing import List
import pyodbc
import os

from models import Message

load_dotenv()



class Database:
    """
    A singleton class for managing a connection to a SQL Server database.

    Usage:
    ------
    1. Import the Database class from this module.
    2. Call the `get_instance` method to get the singleton instance of the class.
    3. Use the `get_all_messages_not_sent` method to retrieve all messages that have not been sent from the Messages table.

    Example:
    --------
    ```
    from database import Database

    # Get the singleton instance of the Database class
    db = Database.get_instance()

    # Retrieve all messages that have not been sent from the Messages table
    messages = db.get_all_messages_not_sent()
    ```

    Attributes:
    ----------
    connection_string (str): The connection string for the SQL Server database.
    connection (pyodbc.Connection): The connection object used to connect to the database.
    instance (Database): The singleton instance of the class.
    """

    __instance = None

    @staticmethod
    def get_instance():
        if Database.__instance is None:
            Database()
        return Database.__instance

    def __init__(self):
        if Database.__instance is not None:
            raise Exception("Database class is a singleton!")
        else:
            # Set up a connection to the SQL Server database

            self.server = os.environ.get('DB_SERVER')
            self.database = os.environ.get('DB_NAME')
            self.username = os.environ.get('DB_USERNAME')
            self.password = os.environ.get('DB_PASSWORD')
            self.cnxn = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={self.username};"
                f"PWD={self.password}"
            )
            Database.__instance = self

    def __del__(self):
        self.cnxn.close()

    def get_all_messages_not_sent(self) -> List[Message]:
        """
         Retrieves all messages that have not been sent from the database.

         Returns:
             A list of dictionaries, where each dictionary represents a row from the query result, with column names as keys and row values as values.
         """
        cursor = self.cnxn.cursor()
        # Execute the SQL query to retrieve all messages that have not been sent
        cursor.execute("SELECT * FROM dbo.GetAllMessagesNotSend()")

        # Fetch all rows returned by the query
        rows = cursor.fetchall()

        # Get the column names from the cursor description
        columns = [column[0] for column in cursor.description]

        # Convert the rows to a list of dictionaries
        messages = []
        for row in rows:
            message_dict = {}
            # enumerate() function to get the index of the current column name
            for i, column in enumerate(columns):
                message_dict[column] = row[i]
            message = Message(**message_dict)
            messages.append(message)
        # Return the result
        return messages

    def update_message_sent_time(self, message_id: int, sent_time: datetime) -> bool:
        """
        Updates the sent time of a message with the specified ID in the database.

        Args:
            message_id: The ID of the message to update.
            sent_time: The sent time to set for the message.
        """
        try:
            with self.cnxn.cursor() as cursor:
                cursor.execute("EXEC dbo.UpdateSendMessageById @id=?, @sentTime=?", message_id, sent_time)
                self.cnxn.commit()
                return True
        except pyodbc.Error as e:
            print(f"Error updating message sent time: {e}")
            return False
