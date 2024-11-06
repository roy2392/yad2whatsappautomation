import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='../.env')

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

# City mapping dictionary
CITIES = {
        'הרצליה': 6400,
        'תל אביב': 5000,
        'רמת גן': 8600,
        'חיפה': 4000,
        'ירושלים': 3000,
        'רעננה': 8700,
        'כפר סבא': 9700,
        'נתניה': 7400,
        'פתח תקווה': 7900,
        'הוד השרון': 6200
}

def get_url(city_name: str, min_rooms: float, max_rooms: float, min_price: int, max_price: int):
    """
    Get listings based on specified parameters

    Args:
        city_name: Name of the city in Hebrew
        min_rooms: Minimum number of rooms
        max_rooms: Maximum number of rooms
        min_price: Minimum price
        max_price: Maximum price
    """
    if city_name not in CITIES:
        raise ValueError(f"City '{city_name}' not found in supported cities")
    
    url = "https://gw.yad2.co.il/feed-search-legacy/realestate/rent"
    params = {
            'topArea': 19,
            'area': 54,
            'city': CITIES[city_name],
            'rooms': f'{min_rooms}-{max_rooms}',
            'price': f'{min_price}-{max_price}',
            'forceLdLoad': True
    }
    response = requests.get(url, params=params)
    return response.json()

def format_listing(item):
    listing_url = f"https://www.yad2.co.il/real-estate/rent/{item['id']}"
    
    # Extract price if available
    price = item.get('price', 'Price not specified')
    if isinstance(price, str):
        price_text = price
    else:
        price_text = f"{price:,} ₪" if price else 'Price not specified'
    
    return (
            f"*New Listing*\n"
            f"📍 Location: {item['row_1']}\n"
            f"🏘️ Area: {item['row_2']}\n"
            f"📊 Details: {item['row_3']}\n"
            f"💰 Price: {price_text}\n"
            f"🔗 Link: {listing_url}\n"
            f"-------------------"
    )

def get_listings(city_name: str, min_rooms: float, max_rooms: float, min_price: int, max_price: int):
    response = get_url(city_name, min_rooms, max_rooms, min_price, max_price)
    feed_items = response["data"]["feed"]["feed_items"]
    formatted_listings = []
    
    for item in feed_items:
        if item["type"] == "ad":
            formatted_listings.append(format_listing(item))
    
    return formatted_listings

def send_whatsapp(city_name: str, min_rooms: float, max_rooms: float, min_price: int, max_price: int):
    client = Client(account_sid, auth_token)
    listings = get_listings(city_name, min_rooms, max_rooms, min_price, max_price)
    
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
    # Example usage
    city_name = "כפר סבא"  # City name in Hebrew
    min_rooms = 2
    max_rooms = 4
    min_price = 0
    max_price = 5000
    
    send_whatsapp(city_name, min_rooms, max_rooms, min_price, max_price)

if __name__ == "__main__":
    main()
