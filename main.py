"""
ISS Overhead Notifier

Author: Alan
Date: September 20th 2024

This project uses data from the following APIS to check if the International Space Station (ISS) is above us.
If it is, it sends an email to the user.
ISS-now API: http://api.open-notify.org/iss-now.json
Sunset-Sunrise API: https://sunrise-sunset.org/api
"""
import smtplib
import time
from datetime import datetime

import requests

# Set the location data
LATITUDE = 0  # Float with your location latitude
LONGITUDE = 0  # Float with your location longitude
# Set the email data
EMAIL = "test@gmail.com"
PASSWORD = "password"
HOST = "smtp.gmail.com"
PORT = 587


def is_iss_close():
    """
    Uses the api iss_now to check if ISS is near our location
    :return: Return True if it is, otherwise, False
    """
    # Get the data from the API
    response = requests.get(url="http://api.open-notify.org/iss-now.json")

    # Store the data
    data = response.json()

    # Get the
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    if LONGITUDE - 5 <= iss_longitude <= LONGITUDE + 5 and LATITUDE - 5 <= iss_latitude <= LATITUDE + 5:

        return True

    else:
        return False


def is_dark():
    """
    Uses the api sunrise-sunset to check if our current time coincides with the city's sunset and sunrise time.
    :return: Returns True if it coincides, otherwise False
    """
    # Set parameters for the json request
    parameters = {"lng": LONGITUDE, "lat": LATITUDE, "formatted": 0}

    # Get data using requests.get
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)

    # Raises an error if we get one
    response.raise_for_status()

    # Stores the data into a json
    data = response.json()

    # Splits the data until we get the hour
    sunrise_time = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_time = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # Get the date of today
    time_now = datetime.now()

    # Get the hour
    hour_now = time_now.hour

    # With the data, we check if it's dark
    if sunset_time == hour_now or sunrise_time == hour_now:

        return True

    else:

        return False


def send_email():
    """
    Sends an email to ourselves, saying to look up
    :return:
    """
    with smtplib.SMTP(host=HOST, port=PORT) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg="Subject:Hey!\n\nLook up!")


while True:

    # So it does this every 60 seconds
    time.sleep(60)

    # If it's dark and the iss is close, then it will send an email
    if is_dark() and is_iss_close():
        send_email()
    else:
        print("Not yet")
