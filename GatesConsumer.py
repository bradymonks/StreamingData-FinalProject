"""
Brady Monks
2/22/23

    This program listens for work messages contiously. 
    Start multiple versions to add more workers.  


"""
import smtplib
from email.message import EmailMessage
import tomli  # requires Python 3.11
import pprint

## Create Email Function

def createAndSendEmailAlert(email_subject: str, email_body: str):
    print(email_body)
    print(email_subject)
    """Read outgoing email info from a TOML config file"""

    with open(".env.toml", "rb") as file_object:
        secret_dict = tomli.load(file_object)
    pprint.pprint(secret_dict)

    # basic information

    host = secret_dict["outgoing_email_host"]
    port = secret_dict["outgoing_email_port"]
    outemail = secret_dict["outgoing_email_address"]
    outpwd = secret_dict["outgoing_email_password"]

    # Create an instance of an EmailMessage

    msg = EmailMessage()
    msg["From"] = secret_dict["outgoing_email_address"]
    msg["To"] = secret_dict["outgoing_email_address"]
    msg["Reply-to"] = secret_dict["outgoing_email_address"]
    email_subject1 = email_subject
    email_body1 = email_body

    msg["Subject"] = email_subject1
    msg.set_content(email_body1)

    print("========================================")
    print(f"Prepared Email Message: ")
    print("========================================")
    print()
    print(f"{str(msg)}")
    print("========================================")
    print()

    # Communications can fail, so use:

    # try -   to execute the code
    # except - when you get an Exception, do something else
    # finally - clean up regardless

    # Create an instance of an email server, enable debug messages

    server = smtplib.SMTP(host)
    server.set_debuglevel(2)

    print("========================================")
    print(f"SMTP server created: {str(server)}")
    print("========================================")
    print()

    try:
        print()
        server.connect(host, port)  # 465
        print("========================================")
        print(f"Connected: {host, port}")
        print("So far so good - will attempt to start TLS")
        print("========================================")
        print()

        server.starttls()
        print("========================================")
        print(f"TLS started. Will attempt to login.")
        print("========================================")
        print()

        try:
            server.login(outemail, outpwd)
            print("========================================")
            print(f"Successfully logged in as {outemail}.")
            print("========================================")
            print()

        except smtplib.SMTPHeloError:
            print("The server did not reply properly to the HELO greeting.")
            exit()
        except smtplib.SMTPAuthenticationError:
            print("The server did not accept the username/password combination.")
            exit()
        except smtplib.SMTPNotSupportedError:
            print("The AUTH command is not supported by the server.")
            exit()
        except smtplib.SMTPException:
            print("No suitable authentication method was found.")
            exit()
        except Exception as e:
            print(f"Login error. {str(e)}")
            exit()

        try:
            server.send_message(msg)
            print("========================================")
            print(f"Message sent.")
            print("========================================")
            print()
        except Exception as e:
            print()
            print(f"ERROR: {str(e)}")
        finally:
            server.quit()
            print("========================================")
            print(f"Session terminated.")
            print("========================================")
            print()

    # Except if we get an Exception (we call e)

    except ConnectionRefusedError as e:
        print(f"Error connecting. {str(e)}")
        print()

    except smtplib.SMTPConnectError as e:
        print(f"SMTP connect error. {str(e)}")
        print()

import pika
import sys
import time
import csv
import statistics

# create list for running totals

HyVee_Totals = []
HyVee_Count = 0
GEHA_Totals = []
GEHA_Count = 0
TMobile_Totals = []
TMobile_Count = 0
CommunityAmerica_Totals = []
CommunityAmerica_Count = 0
Founders_Totals = []
Founders_Count = 0
Tower_Totals = []
Tower_Count = 0

# define a callback function to be called when a message is received for the HyVee Gate
def HyVee_callback(ch, method, properties, body):
    """ Define behavior on getting a message."""
    # Decode the binary message body to a string
    message = body.decode().strip()
    try:
        # Split the message at the comma
        timestamp, entries = message.split(',')
        # Remove any leading or trailing white space
        timestamp = timestamp.strip()
        entries = entries.strip()
        # convert the temperature to type float
        entries = float(entries)
    except ValueError:
        # ignore the error and continue the process
        pass
    print(f" [x] Received HyVee Gate at {body.decode()} new entries")
    
     # Check if the message is type float
    if isinstance(entries, float):
        HyVee_Totals.append(entries)

    # Identify HyVee_Count as a global variable
    global HyVee_Count

    # add to count 

    HyVee_Count += 1

    # check to see if the most current entry is an outlier

    if HyVee_Count % 5 == 0:
        # define a constant for the outlier threshold
        OUTLIER_THRESHOLD = 2

        # calculate the average and standard deviation of the HyVee_Totals list
        mean = statistics.mean(HyVee_Totals)
        stdev = statistics.stdev(HyVee_Totals)

        # check if the most recent entry is an upper outlier and create cmd prompt alert and email alert
        if entries > mean + OUTLIER_THRESHOLD * stdev:
            alert = "***** There is a surge of "+ str(entries) + " entries at the HyVee Gate at "+ timestamp + "send help."
            print(alert)
            subject_str = "HyVee Gate"
            content_str = alert
            createAndSendEmailAlert(email_subject=subject_str, email_body=content_str)
        # check if the most recent entry is a lower outlier and create cmd prompt alert and email alert
        elif entries < mean - OUTLIER_THRESHOLD * stdev:
            alert = "***** There is a decrease of " + str(entries) + " entries at the HyVee Gate at " + timestamp +  "return workers."
            print(alert)
            subject_str = "HyVee Gate"
            content_str = alert
            createAndSendEmailAlert(email_subject=subject_str, email_body=content_str)


    # simulate work by sleeping for the number of dots in the message
    time.sleep(body.count(b"."))
    # when done with task, tell the user
    print(" [x] Done.")
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# define a callback function to be called when a message is received for the GEHA Gate
def GEHA_callback(ch, method, properties, body):
    """ Define behavior on getting a message."""
    # Decode the binary message body to a string
    message = body.decode().strip()
    try:
        # Split the message at the comma
        timestamp, entries = message.split(',')
        # Remove any leading or trailing white space
        timestamp = timestamp.strip()
        entries = entries.strip()
        # convert the temperature to type float
        entries = float(entries)
    except ValueError:
        # ignore the error and continue the process
        pass
    print(f" [x] Received GEHA Gate at {body.decode()} new entries")
    
     # Check if the message is type float
    if isinstance(entries, float):
        GEHA_Totals.append(entries)

    # Identify HyVee_Count as a global variable
    global GEHA_Count

    # add to count 

    GEHA_Count += 1

    # check to see if the most current entry is an outlier

    if GEHA_Count % 5 == 0:
        # define a constant for the outlier threshold
        OUTLIER_THRESHOLD = 2

        # calculate the average and standard deviation of the GEHA_Totals list
        mean = statistics.mean(GEHA_Totals)
        stdev = statistics.stdev(GEHA_Totals)

        # check if the most recent entry is an upper outlier and create cmd prompt alert and email alert
        if entries > mean + OUTLIER_THRESHOLD * stdev:
            alert = "***** There is a surge of "+ str(entries) + " entries at the GEHA Gate at "+ timestamp + "send help."
            print(alert)
            subject_str = "GEHA Gate"
            content_str = alert
            createAndSendEmailAlert(email_subject=subject_str, email_body=content_str)
        # check if the most recent entry is a lower outlier and create cmd prompt alert and email alert
        elif entries < mean - OUTLIER_THRESHOLD * stdev:
            alert = "***** There is a decrease of " + str(entries) + " entries at the GEHA Gate at " + timestamp +  "return workers."
            print(alert)
            subject_str = "GEHA Gate"
            content_str = alert
            createAndSendEmailAlert(email_subject=subject_str, email_body=content_str)

    # simulate work by sleeping for the number of dots in the message
    time.sleep(body.count(b"."))
    # when done with task, tell the user
    print(" [x] Done.")
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)
   
# define a callback function to be called when a message is received for the T-Mobile Gate
def TMobile_callback(ch, method, properties, body):
    """ Define behavior on getting a message."""
    # Decode the binary message body to a string
    message = body.decode().strip()
    try:
        # Split the message at the comma
        timestamp, entries = message.split(',')
        # Remove any leading or trailing white space
        timestamp = timestamp.strip()
        entries = entries.strip()
        # convert the temperature to type float
        entries = float(entries)
    except ValueError:
        # ignore the error and continue the process
        pass
    print(f" [x] Received T-Mobile Gate at {body.decode()} new entries")
    
     # Check if the message is type float
    if isinstance(entries, float):
        TMobile_Totals.append(entries)

    # Identify HyVee_Count as a global variable
    global TMobile_Count

    # add to count 

    TMobile_Count += 1

    # check to see if the most current entry is an outlier

    if TMobile_Count % 5 == 0:
        # define a constant for the outlier threshold
        OUTLIER_THRESHOLD = 2

        # calculate the average and standard deviation of the TMobile_Totals list
        mean = statistics.mean(TMobile_Totals)
        stdev = statistics.stdev(TMobile_Totals)

        # check if the most recent entry is an upper outlier and create cmd prompt alert and email alert
        if entries > mean + OUTLIER_THRESHOLD * stdev:
            alert = "***** There is a surge of "+ str(entries) + " entries at the T-Mobile Gate at "+ timestamp + "send help."
            print(alert)
            subject_str = "T-Mobile Gate"
            content_str = alert
            createAndSendEmailAlert(email_subject=subject_str, email_body=content_str)
        # check if the most recent entry is a lower outlier and create cmd prompt alert and email alert
        elif entries < mean - OUTLIER_THRESHOLD * stdev:
            alert = "***** There is a decrease of " + str(entries) + " entries at the T-Mobile Gate at " + timestamp +  "return workers."
            print(alert)
            subject_str = "T-Mobile Gate"
            content_str = alert
            createAndSendEmailAlert(email_subject=subject_str, email_body=content_str)


    # simulate work by sleeping for the number of dots in the message
    time.sleep(body.count(b"."))
    # when done with task, tell the user
    print(" [x] Done.")
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)
   
# define a callback function to be called when a message is received for the CommunityAmerica Gate
def CommunityAmerica_callback(ch, method, properties, body):
    """ Define behavior on getting a message."""
    # Decode the binary message body to a string
    message = body.decode().strip()
    try:
        # Split the message at the comma
        timestamp, entries = message.split(',')
        # Remove any leading or trailing white space
        timestamp = timestamp.strip()
        entries = entries.strip()
        # convert the temperature to type float
        entries = float(entries)
    except ValueError:
        # ignore the error and continue the process
        pass
    print(f" [x] Received CommunityAmerica Gate at {body.decode()} new entries")
    
     # Check if the message is type float
    if isinstance(entries, float):
        CommunityAmerica_Totals.append(entries)

    # Identify HyVee_Count as a global variable
    global CommunityAmerica_Count

    # add to count 

    CommunityAmerica_Count += 1

    # check to see if the most current entry is an outlier

    if CommunityAmerica_Count % 5 == 0:
        # define a constant for the outlier threshold
        OUTLIER_THRESHOLD = 2

        # calculate the average and standard deviation of the CommunityAmerica_Totals list
        mean = statistics.mean(CommunityAmerica_Totals)
        stdev = statistics.stdev(CommunityAmerica_Totals)

        # check if the most recent entry is an upper outlier and create cmd prompt alert and email alert
        if entries > mean + OUTLIER_THRESHOLD * stdev:
            alert = "***** There is a surge of "+ str(entries) + " entries at the CommunityAmerica Gate at "+ timestamp + "send help."
            print(alert)
            subject_str = "CommunityAmerica Gate"
            content_str = alert
            createAndSendEmailAlert(email_subject=subject_str, email_body=content_str)
        # check if the most recent entry is a lower outlier and create cmd prompt alert and email alert
        elif entries < mean - OUTLIER_THRESHOLD * stdev:
            alert = "***** There is a decrease of " + str(entries) + " entries at the CommunityAmerica Gate at " + timestamp +  "return workers."
            print(alert)
            subject_str = "CommunityAmerica Gate"
            content_str = alert
            createAndSendEmailAlert(email_subject=subject_str, email_body=content_str)

    # simulate work by sleeping for the number of dots in the message
    time.sleep(body.count(b"."))
    # when done with task, tell the user
    print(" [x] Done.")
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)
   
# define a callback function to be called when a message is received for the Founder's Plaza Gate
def Founders_callback(ch, method, properties, body):
    """ Define behavior on getting a message."""
    # Decode the binary message body to a string
    message = body.decode().strip()
    try:
        # Split the message at the comma
        timestamp, entries = message.split(',')
        # Remove any leading or trailing white space
        timestamp = timestamp.strip()
        entries = entries.strip()
        # convert the temperature to type float
        entries = float(entries)
    except ValueError:
        # ignore the error and continue the process
        pass
    print(f" [x] Received Founder's Plaza Gate at {body.decode()} new entries")
    
     # Check if the message is type float
    if isinstance(entries, float):
        Founders_Totals.append(entries)

    # Identify HyVee_Count as a global variable
    global Founders_Count

    # add to count 

    Founders_Count += 1

    # check to see if the most current entry is an outlier

    if Founders_Count % 5 == 0:
        # define a constant for the outlier threshold
        OUTLIER_THRESHOLD = 2

        # calculate the average and standard deviation of the Founders_Totals list
        mean = statistics.mean(Founders_Totals)
        stdev = statistics.stdev(Founders_Totals)

        # check if the most recent entry is an upper outlier and create cmd prompt alert and email alert
        if entries > mean + OUTLIER_THRESHOLD * stdev:
            alert = "***** There is a surge of "+ str(entries) + " entries at the Founder's Plaza Gate at "+ timestamp + "send help."
            print(alert)
            subject_str = "Founder's Plaza Gate"
            content_str = alert
            createAndSendEmailAlert(email_subject=subject_str, email_body=content_str)
        # check if the most recent entry is a lower outlier and create cmd prompt alert and email alert
        elif entries < mean - OUTLIER_THRESHOLD * stdev:
            alert = "***** There is a decrease of " + str(entries) + " entries at the Founder's Plaza Gate at " + timestamp +  "return workers."
            print(alert)
            subject_str = "Founder's Plaza Gate"
            content_str = alert
            createAndSendEmailAlert(email_subject=subject_str, email_body=content_str)

    # simulate work by sleeping for the number of dots in the message
    time.sleep(body.count(b"."))
    # when done with task, tell the user
    print(" [x] Done.")
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)
   
# define a callback function to be called when a message is received for the Tower Gate
def Tower_callback(ch, method, properties, body):
    """ Define behavior on getting a message."""
    # Decode the binary message body to a string
    message = body.decode().strip()
    try:
        # Split the message at the comma
        timestamp, entries = message.split(',')
        # Remove any leading or trailing white space
        timestamp = timestamp.strip()
        entries = entries.strip()
        # convert the temperature to type float
        entries = float(entries)
    except ValueError:
        # ignore the error and continue the process
        pass
    print(f" [x] Received Tower Gate at {body.decode()} new entries")
    
     # Check if the message is type float
    if isinstance(entries, float):
        Tower_Totals.append(entries)

    # Identify HyVee_Count as a global variable
    global Tower_Count

    # add to count 

    Tower_Count += 1

    # check to see if the most current entry is an outlier
    
    if Tower_Count % 5 == 0:
        # define a constant for the outlier threshold
        OUTLIER_THRESHOLD = 2

        # calculate the average and standard deviation of the Tower_Totals list
        mean = statistics.mean(Tower_Totals)
        stdev = statistics.stdev(Tower_Totals)

        # check if the most recent entry is an upper outlier and create cmd prompt alert and email alert
        if entries > mean + OUTLIER_THRESHOLD * stdev:
            alert = "***** There is a surge of "+ str(entries) + " entries at the Tower Gate at "+ timestamp + "send help."
            print(alert)
            subject_str = "Tower Gate"
            content_str = alert
            createAndSendEmailAlert(email_subject=subject_str, email_body=content_str)
        # check if the most recent entry is a lower outlier and create cmd prompt alert and email alert
        elif entries < mean - OUTLIER_THRESHOLD * stdev:
            alert = "***** There is a decrease of " + str(entries) + " entries at the Tower Gate at " + timestamp +  "return workers."
            print(alert)
            subject_str = "Tower Gate"
            content_str = alert
            createAndSendEmailAlert(email_subject=subject_str, email_body=content_str)

    # simulate work by sleeping for the number of dots in the message
    time.sleep(body.count(b"."))
    # when done with task, tell the user
    print(" [x] Done.")
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main(hn: str = "localhost", qn_HyVee: str = "HyVee_Gate", qn_GEHA: str = "GEHA_Gate", qn_TMobile: str = "T-Mobile_Gate",qn_CA: str = "CommunityAmerica_Gate",qn_Founders: str = "FoundersPlaza_Gate",qn_Tower: str = "Tower_Gate"):
    """ Continuously listen for task messages on named queues."""

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))
    except Exception as e:
        print()
        print("ERROR: connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says: {e}")
        print()
        sys.exit(1)

    try:
        channel_a = connection.channel()
        channel_a.queue_declare(queue=qn_HyVee, durable=True)
        channel_a.basic_qos(prefetch_count=1)
        channel_a.basic_consume(queue=qn_HyVee, on_message_callback=HyVee_callback)

        channel_b = connection.channel()
        channel_b.queue_declare(queue=qn_GEHA, durable=True)
        channel_b.basic_qos(prefetch_count=1)
        channel_b.basic_consume(queue=qn_GEHA, on_message_callback=GEHA_callback)

        channel_c = connection.channel()
        channel_c.queue_declare(queue=qn_TMobile, durable=True)
        channel_c.basic_qos(prefetch_count=1)
        channel_c.basic_consume(queue=qn_TMobile, on_message_callback=TMobile_callback)

        channel_d = connection.channel()
        channel_d.queue_declare(queue=qn_CA, durable=True)
        channel_d.basic_qos(prefetch_count=1)
        channel_d.basic_consume(queue=qn_CA, on_message_callback=CommunityAmerica_callback)

        channel_e = connection.channel()
        channel_e.queue_declare(queue=qn_Founders, durable=True)
        channel_e.basic_qos(prefetch_count=1)
        channel_e.basic_consume(queue=qn_Founders, on_message_callback=Founders_callback)

        channel_f = connection.channel()
        channel_f.queue_declare(queue=qn_Tower, durable=True)
        channel_f.basic_qos(prefetch_count=1)
        channel_f.basic_consume(queue=qn_Tower, on_message_callback=Tower_callback)

        print(" [*] Ready for work. To exit press CTRL+C")

        channel_a.start_consuming()
        channel_b.start_consuming()
        channel_c.start_consuming()
        channel_d.start_consuming()
        channel_e.start_consuming()
        channel_f.start_consuming()

    except Exception as e:
        print()
        print("ERROR: something went wrong.")
        print(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print(" User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        print("\nClosing connection. Goodbye.\n")
        connection.close()



# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # call the main function for the HyVee Gate
    main("localhost", "HyVee_Gate")

    # call the main function for the GEHA Gate
    main("localhost", "GEHA_Gate")

    # call the main function for the T-Mobile Gate
    main("localhost", "T-Mobile_Gate")

    # call the main function for the CommunityAmerica Gate
    main("localhost", "CommunityAmerica_Gate")

    # call the main function for the Founder's Plaza Gate
    main("localhost", "FoundersPlaza_Gate")

    # call the main function for the Tower Gate
    main("localhost", "Tower_Gate")
