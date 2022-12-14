import requests
from datetime import datetime
import time
from config import *
import smtplib

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}


def get_iss_vis(lat, long):
    if (lat + 5 == MY_LAT or lat - 5 == MY_LAT) and (long + 5 == MY_LONG or long - 5 == MY_LONG):
        return True


def get_hours():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    return {'sunrise': sunrise, 'sunset': sunset}


def sendmail(addr, text):
    my_email = email
    my_password = password
    connection = smtplib.SMTP('smtp.office365.com', 587)
    connection.starttls()
    connection.login(user=my_email, password=my_password)
    connection.ehlo()
    connection.sendmail(from_addr=my_email,
                        to_addrs=addr,
                        msg=f'Subject:ISS is near!\n\n\n{text}'
                        )


def get_iss():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    return {'lat': iss_latitude, 'long': iss_longitude}


running = True

while running:
    iss_latitude = get_iss()['lat']
    iss_longitude = get_iss()['long']

    sunrise = get_hours()['sunrise']
    sunset = get_hours()['sunset']

    time_now = datetime.now()
    time_now_hour = time_now.hour
    email_sent = False

    while get_iss_vis(iss_latitude, iss_longitude) and not email_sent:
        # print('ISS is near and its night!')
        sendmail('joachim.lehmann@googlemail.com', 'The ISS is nearby and its night!')
        # set mail sent to True
        email_sent = True

    print(f'ISS at lat:{iss_latitude}, long:{iss_longitude}', end='\r', flush=True)
    email_sent = False
    time.sleep(2)
