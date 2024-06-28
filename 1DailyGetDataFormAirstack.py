import asyncio
import nest_asyncio
import json
import sys
from airstack.execute_query import AirstackClient

nest_asyncio.apply()

# Load API key from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    api_key = config['airstack_api_key']

api_client = AirstackClient(api_key=api_key)

query = """
query MyQuery {
  TrendingCasts(
    input: {timeFrame: one_day, blockchain: ALL, criteria: social_capital_value, limit: 1}
  ) {
    TrendingCast {
      cast {
        castedAtTimestamp
        embeds
        hash
        fid
        text
        numberOfRecasts
        numberOfLikes
        numberOfReplies
        castedBy {
          fnames
        }
        channel {
          channelId
          name
        }
        socialCapitalValue{
          formattedValue
          rawValue
        }
      }
    }
  }
}
"""

def safe_print(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2).encode('utf-8').decode(sys.stdout.encoding, 'ignore'))

async def main():
    all_data = []
    execute_query_client = api_client.create_execute_query_object(query=query)
    query_response = await execute_query_client.execute_paginated_query()
   
    if query_response.error is not None:
        raise Exception(query_response.error.message)
    
    all_data.extend(query_response.data['TrendingCasts']['TrendingCast'])
    safe_print(query_response.data)  # Using safe_print instead of print
    
    page_limit = int(config['page_limit']) # Set the maximum number of pages to fetch
    current_page = 0  # Initialize page counter
    
    while query_response.has_next_page and current_page < page_limit:
        print("Fetching next page...")
        query_response = await query_response.get_next_page
        if query_response.data:
            all_data.extend(query_response.data['TrendingCasts']['TrendingCast'])
            safe_print(query_response.data)  # Using safe_print instead of print
        current_page += 1  # Increment the page counter
    
    with open('AllTrendOutput.txt', 'w', encoding='utf-8') as file:
        json.dump(all_data, file, ensure_ascii=False, indent=4)

asyncio.run(main())