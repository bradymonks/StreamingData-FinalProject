# StreamingData-FinalProject

Author: Brady Monks

Date: February 22, 2023

# Overview

My passion growing up has been sports. I rode that passion playing-wise until the fall of 2021, when I retired from college football. However, sports still make my brain tick, and I want to continue being a part of the sports world as I transition to a working man. My dream job is to work for the Kansas City Chiefs, and I wanted to incorporate that into this project. Using RabbitMQ and Python, I want to create a consumer/producer process that monitors the entrance of fans on gameday. How I can do that is to set up a csv file that has 30 second intervals and 6 columns one for each of the gates (HyVee, CommunityAmerica, GEHA, T-Mobile, Tower, and Founder's Plaza) of Arrowhead Stadium, where the Chiefs play. Using a similar setup to our Smoker process, I will get updates every 30 seconds that tells me how many fans have gone through each gate in the last 30 seconds. If there is a surge of fans at a certain gate, it will trigger an alert that will let Security personnel and Ticket Scanners on stand-by know they are needed a certain locations to help the surge of people get into the game smoothly. The four main gates are HyVee, T-Mobile, GEHA, and CommunityAmerica. They are located at the four corners of the stadium. They are where the majority of fans will enter the game through. Tower Gate and Founder's Plaza Gate will be located on the two long sides of the stadium. These two gates will have less people coming in through them. 

# Generated CSV file

I was having trouble getting the desired numbers in each column using faker, so I resolved to going in Excel and using the RANDBETWEEN() function at certain time intervals, that I know from experience, that the majority of people come in. 

# Producer and Consumer Set up

For my project, I wanted to go with one producer reading through the csv file and setting the entry totals to 6 different consumers, each with their own queue. 

## Producer

Every time I send messages out, my producer will go through the csv file and read 7 values - timestamp and entry totals for the six gates (HyVee, T-Mobile, GEHA, CommunityAmerica, Tower, and Founder's Plaza). 

## Consumers

Within each consumer, a running total will be kept for the entry totals of each gate. What I will be monitoring is if an interval is an outlier of the running average. If it is way above the running average, then we will send an email (alert) to extra staff members letting them know to go to a gate to help facilitate fans into the stadium. If an interval is an outlier below the running average, then we will send an email (alert) to those staff members, letting them know they aren't needed at those gates anymore, and they may return back to where they were.
  