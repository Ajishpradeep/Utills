import requests
import json
import os
import re
import time
from urllib.parse import urlparse

# Define a list of products to search for
product_queries = ['Groceries', 'Snacks', 'Soft Drinks', 'Canned food', 'Chocolate', 'Dairy Products', 'Baked Goods',
                   'Frozen Foods', 'Condiments', 'Breakfast Cereals']

# Define the API key
api_key = '05beb6bbac7acedf5f529d3951ee7b4e' #expired sample API

# Initialize an empty list to store results
all_results = []

# Initialize a dictionary to store count of results per category
results_count = {query: 0 for query in product_queries}

# Function to sanitize file names
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|[],()-]', "", name)

# Function to fetch results for a query with pagination
def fetch_results_for_query(query, max_results=500):
    results = []
    page = 1
    while len(results) < max_results:
        payload = {
            'api_key': api_key,
            'query': query,
            'page': page
        }

        response = requests.get('https://api.scraperapi.com/structured/amazon/search', params=payload)

        if response.status_code != 200:
            print(f"Failed to fetch results for query: {query}, page: {page}")
            break

        data = response.json()
        if 'results' not in data or not data['results']:
            # for query, count in results_count.items():
            print(f"Fetched {len(results)} results for query: {query}")  # Print number of results fetched
            break

        current_results = data['results']
        results.extend(current_results)

        # Increment count of results fetched
        results_count[query] += len(current_results)

        # Check if we have enough results
        if len(results) >= max_results:
            results = results[:max_results]
            break

        page += 1
        time.sleep(1)  # Be polite and avoid hitting the API too frequently

    return results

# Function to save images from URLs
# Function to save images from URLs
def save_images(results, directory='images'):
    if not os.path.exists(directory):
        os.makedirs(directory)

    total_images = len(results)
    saved_count = 0

    for index, result in enumerate(results, start=1):
        image_url = result.get('image', '')
        title = result.get('title', 'unknown')
        query = result.get('category', 'unknown')

        if image_url:
            try:
                response = requests.get(image_url, stream=True)
                if response.status_code == 200:
                    # Get content type from response headers
                    content_type = response.headers.get('content-type')
                    # Determine file extension based on content type
                    if content_type:
                        extension = re.findall(r'image/(jpeg|jpg|png|gif)', content_type)
                        if extension:
                            extension = '.' + extension[0]
                        else:
                            extension = '.jpg'  # Default to .jpg if content type not recognized
                    else:
                        extension = '.jpg'  # Default to .jpg if no content type

                    # Construct new filename using category and title
                    filename = f"{sanitize_filename(query)}_{sanitize_filename(title)}{extension}"

                    # Save image to file
                    with open(os.path.join(directory, filename), 'wb') as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            f.write(chunk)
                    
                    saved_count += 1
                    print(f"Saved image {filename} [{saved_count}/{total_images}]")
            except Exception as e:
                print(f"Error saving image {image_url}: {str(e)}")

        # Add a small delay to be polite to the server
        time.sleep(0.5)

    print(f"All {saved_count} images saved successfully.")



# Iterate over each product query
for query in product_queries:
    print(f"Fetching results for: {query}")
    query_results = fetch_results_for_query(query)
    for r in query_results:
        result_dict = {
            "category": query,
            "title": r.get('name', 'unknown'),
            "image": r.get('image', ''),
        }
        all_results.append(result_dict)

# Save the result list to a JSON file
with open('results.json', 'w') as json_file:
    json.dump(all_results, json_file, indent=4)
print("JSON Saved")

# Print results count for each category
for query, count in results_count.items():
    print(f"Fetched {count} results for {query}")

# Save images from URLs
save_images(all_results)
print("Images saved")