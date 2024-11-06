import requests
import pandas as pd
from typing import Dict, List

def get_cities_mapping() -> Dict[str, int]:
    url = "https://gw.yad2.co.il/feed-search-legacy/realestate/rent"
    response = requests.get(url)
    data = response.json()
    
    # Extract cities data from the response
    cities_data = data['data']['feed']['feed_search']['cities']
    
    # Create a mapping dictionary
    cities_mapping = {}
    for city in cities_data:
        cities_mapping[city['name']] = city['city_id']
    
    return cities_mapping

def create_cities_table():
    cities_mapping = get_cities_mapping()
    
    # Convert to DataFrame for better visualization
    df = pd.DataFrame(list(cities_mapping.items()), columns=['City Name', 'City ID'])
    df = df.sort_values('City Name')
    
    # Display the first few rows
    print("\nSample of the cities mapping:")
    print(df.head(10))
    
    # Save to CSV
    df.to_csv('.data/yad2_cities_mapping.csv', index=False, encoding='utf-8-sig')
    return df

if __name__ == "__main__":
    df = create_cities_table()
