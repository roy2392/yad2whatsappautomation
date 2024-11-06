import requests
from twilio.rest import Client
import os
import json
import time
from dotenv import load_dotenv

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

def get_url():
    # Hod Hasharon
    url = "https://gw.yad2.co.il/feed-search-legacy/realestate/rent"
    params = {
        'topArea': 19,
        'area': 54,
        'city': 9700,
        'rooms': '2-4',
        'price': '0-5000',
        'forceLdLoad': True
    }
    response = requests.get(url, params=params)
    return response.json()

def sorted_items():
    response = get_url()
    feed_items = response["data"]["feed"]["feed_items"]
    result = feed_items
    with open("new.txt", "w") as f:
        for item in result:
            if item["type"] == "ad":
                f.write(f'{item["row_1"]} {item["row_2"]} {item["row_3"]}\n')
    with open('new.txt', 'r') as f:
        lines = f.readlines()
        lines = sorted(set(lines))
    with open('new.txt', 'w') as f:
        f.writelines(lines)
    with open('new.txt', 'r') as new_file:
        new_lines = new_file.readlines()
    diff_lines = []
    diff_lines.append(new_lines)
    return diff_lines

def send_whatsapp():
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=sorted_items(),
        to='whatsapp:+972526000000'
    )
    print(message.sid)

def main():
    send_whatsapp()

if __name__ == "__main__":
    main()
