import json
import requests
import codecs
import os
import sys

def safe_print(obj):
    try:
        print(json.dumps(obj, indent=2, ensure_ascii=False))
    except UnicodeEncodeError:
        print(json.dumps(obj, indent=2, ensure_ascii=True))

# Function to read configuration from config.json
def read_config(file_path):
    with codecs.open(file_path, 'r', 'utf-8') as file:
        return json.load(file)

# Read JSON data from file
def read_json_from_file(file_path):
    print(f"Attempting to read file: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    print(f"File size: {os.path.getsize(file_path)} bytes")

    encodings_to_try = ['utf-8', 'utf-8-sig', 'iso-8859-1']
    
    for encoding in encodings_to_try:
        print(f"Trying to read with {encoding} encoding...")
        try:
            with codecs.open(file_path, 'r', encoding) as file:
                content = file.read()
                print(f"Successfully read with {encoding} encoding")
                print(f"First 100 characters: {content[:100]}")
                json_data = json.loads(content)
                print(f"Successfully parsed JSON data")
                return json_data
        except UnicodeDecodeError as e:
            print(f"UnicodeDecodeError with {encoding}: {e}")
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError with {encoding}: {e}")
        except Exception as e:
            print(f"Unexpected error with {encoding}: {e}")
    
    raise ValueError(f"Unable to read file with any of the attempted encodings: {encodings_to_try}")

# Load configuration
config = read_config('config.json')

# Read the data from your JSON file
data = read_json_from_file('ManualChecked.txt')

filtered_data = [entry for entry in data if entry.get("OpenAICheckRelevant") != "Not"]

# Reformat the data
reformatted_data = []
for entry in filtered_data:
    reformatted_entry = {
        "hash": entry["hash"],
        "username": entry["username"],
        "fid": int(entry["fid"]),
        "text": entry["text"],
        "channel": entry["channel"],
        "tags": entry.get("tags", ""),
        "likes": entry["likes"],
        "replies": entry["replies"],
        "recasts": entry["recasts"],
        "scv": entry["scv"],
        "casted_at": entry["casted_at"]
    }
    reformatted_data.append(reformatted_entry)

# API endpoint from config
url = config['api_url']

# Headers with Bearer token from config
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {config["bearer_token"]}'
}

print("Reformatted data sample:")
safe_print(reformatted_data[:1])

# Send POST request
try:
    response = requests.post(url, headers=headers, json=reformatted_data)
    
    # Check response
    if response.status_code == 200:
        print("Data submitted successfully!")
        print("Response:")
        safe_print(response.json())
    else:
        print(f"Error submitting data. Status code: {response.status_code}")
        print("Response:")
        safe_print(response.text)
except Exception as e:
    print(f"Error during API request: {e}")

# Optionally, write the reformatted data to a file for verification
with codecs.open('reformatted_data.txt', 'w', 'utf-8') as outfile:
    json.dump(reformatted_data, outfile, indent=2, ensure_ascii=False)

print("Process completed.")
print(f"Reformatted data written to reformatted_data.txt (size: {os.path.getsize('reformatted_data.txt')} bytes)")