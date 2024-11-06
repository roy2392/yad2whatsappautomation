# Real-Time Yad2 Real Estate Scraper with Twilio WhatsApp Notifications

This project is a real-time real estate scraper for the Yad2 website that sends new listings via WhatsApp using the Twilio API. The script fetches rental listings from Yad2 for a specific city, processes the data, and sends a notification with the new listings.

## Features

- **Real-Time Data Scraping**: Fetches rental listings from Yad2 in real-time.
- **Data Processing**: Filters and processes the listings to extract relevant information.
- **WhatsApp Notifications**: Sends new listings as WhatsApp messages using the Twilio API.

## Prerequisites

- Python 3.x
- `requests` library
- `twilio` library
- Twilio account with WhatsApp sandbox setup
- Yad2 API access

## Installation

1. Clone this repository:
    ```sh
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Update the Twilio account SID and auth token in the script:
    ```python
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    ```

2. Customize the Yad2 API parameters in the script:
    ```python
    params = {
        'topArea': 19,
        'area': 54,
        'city': 9700,
        'rooms': '2-4',
        'price': '0-5000',
        'forceLdLoad': True
    }
    ```

3. Run the script:
    ```sh python 
    src/python app.py
    ```


