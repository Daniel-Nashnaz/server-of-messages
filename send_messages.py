import datetime
import time
from email_utils import send_email
from singalton_db_connection import Database

db = Database.get_instance()


def start_check_if_there_message_to_send():
    messages = db.get_all_messages_not_sent()
    if not messages:
        print("no more!!!")
        return
    for message in messages:
        # Call the send_email function to send the email
        success = send_email(message.Email, message.Subject, message.Body)
        if not success:
            return
        # email was sent successfully, update the message record in the database
        now = datetime.datetime.now()
        db.update_message_sent_time(message.ID, now.strftime('%Y-%m-%d %H:%M:%S'))
        # Wait for 1.5 seconds before sending the next message
        time.sleep(1.5)
