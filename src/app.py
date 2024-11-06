import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='../.env')

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

def get_url():
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

def format_listing(item):
    listing_url = f"https://www.yad2.co.il/real-estate/rent/{item['id']}"
    return (
            f"*New Listing*\n"
            f"📍 Location: {item['row_1']}\n"
            f"🏘️ Area: {item['row_2']}\n"
            f"📊 Details: {item['row_3']}\n"
            f"🔗 Link: {listing_url}\n"
            f"-------------------"
    )

def get_listings():
    response = get_url()
    feed_items = response["data"]["feed"]["feed_items"]
    formatted_listings = []
    
    for item in feed_items:
        if item["type"] == "ad":
            formatted_listings.append(format_listing(item))
    
    return formatted_listings

def send_whatsapp():
    client = Client(account_sid, auth_token)
    listings = get_listings()
    
    for listing in listings:
        try:
            message = client.messages.create(
                    from_='whatsapp:+14155238886',
                    body=listing,
                    to='whatsapp:+972528978214'
            )
            print(f"Message sent: {message.sid}")
        except Exception as e:
            print(f"Error sending message: {e}")

def main():
    send_whatsapp()

if __name__ == "__main__":
    main()
