# StreamingData-FinalProject

Author: Brady Monks

Date: February 22, 2023

## Requirements

Python version: 3.11+

# Overview

My passion growing up has been sports. I rode that passion playing-wise until the fall of 2021, when I retired from college football. However, sports still make my brain tick, and I want to continue being a part of the sports world as I transition to a working man. My dream job is to work for the Kansas City Chiefs, and I wanted to incorporate that into this project. Using RabbitMQ and Python, I want to create a consumer/producer process that monitors the entrance of fans on gameday. How I can do that is to set up a csv file that has 30 second intervals and 6 columns one for each of the gates (HyVee, CommunityAmerica, GEHA, T-Mobile, Tower, and Founder's Plaza) of Arrowhead Stadium, where the Chiefs play. Using a similar setup to our Smoker process, I will get updates every 30 seconds that tells me how many fans have gone through each gate in the last 30 seconds. If there is a surge of fans at a certain gate, it will trigger an alert that will let Security personnel and Ticket Scanners on stand-by know they are needed a certain locations to help the surge of people get into the game smoothly. The four main gates are HyVee, T-Mobile, GEHA, and CommunityAmerica. They are located at the four corners of the stadium. They are where the majority of fans will enter the game through. Tower Gate and Founder's Plaza Gate will be located on the two long sides of the stadium. These two gates will have less people coming in through them. 

# Generated CSV file

I was having trouble getting the desired numbers in each column using faker, so I resolved to going in Excel and using the RANDBETWEEN() function at certain time intervals, that I know from experience, that the majority of people come in. 

# Producer and Consumer Set up

For my project, I wanted to go with one producer reading through the csv file and sending the entry totals to 6 different consumers, each with their own queue. Similarly to the Smoker project, I took the timestamp and entry totals and combined them into one message for each queue. 

## Producer

Every time I send messages out, my producer will go through the csv file and read 7 values - timestamp and entry totals for the six gates (HyVee, T-Mobile, GEHA, CommunityAmerica, Tower, and Founder's Plaza). 

## Consumers

Within each consumer, a running total will be kept for the entry totals of each gate. What I will be monitoring is if an interval is an outlier of the running average. If it is way above (2.5 standard deviations) the running average, then we will send an email (alert) to extra staff members letting them know to go to a gate to help facilitate fans into the stadium. If an interval is an outlier below (1 standard deviation) the running average, then we will send an email (alert) to those staff members, letting them know they aren't needed at those gates anymore, and they may return back to where they were.

### Email Function

I used the email function from the smoker project. In a real world application, it wouldn't be an email, but rather an update to worker's phones via a mobile app. 

--- surge example email
--- decrease example email

### Created List and Running Totals

In order to monitor changes in entry totals, I had to create variables for each gate. I had two for each gate, a count and a total. The count variable is in there as a ticker to keep track of how many updates we have for each gate. I need that because, although we get updates every 30 seconds, I only want to check if we need to send workers every 2.5 minutes (5 new entries). The totals variable works as a list that we append each entry to and allows us to look at the running average of each gate. 
There are two more variables to help keep track of the workers - Worker_Count and Worker_Recalls. These two, along with the count for each gate, have to be identified as global variables within each callback function to allow me to continually alter them. 

--- counts and totals

### Callback Functions

Each callback function is designed identically, just replacing the gate name each time. In the Tower Gate callback function, I did add two prints at the end - one to let us know how many workers have been sent out and one to let us know how many workers have been recalled. As we receive each message from the producer, the callback splits up the message into two variables - timestamp and entries. This allows me to work with them separately. For each entry total, as long as it's a number, we append it to our totals list for each gate. Once it's been added, it checks to see if it is on it's fifth update since the last check. If it is, then it checks to see if the most recent entry total is 2.5 standard deviations above or 1 standard deviation below the running average (outliers). If either of those are the case, an alert is sent to ensure that workers are being used efficiently, and the Worker_Count and Worker_Recall variables are adjusted accordingly. 

### Received Message

In my received message I kept the format simple as "Gate Name: Timestamp -- ## new entries".
I felt like my eyes were bouncing around when receiving messages so I added dashes to each gate other than CommumityAmerica Gate so each of the timestamps and entry numbers lined up neatly.

-- received message


