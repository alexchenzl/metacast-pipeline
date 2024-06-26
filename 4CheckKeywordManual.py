import openai
import json
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

# Configure OpenAI API key
openai.api_key = config['openai_api_key']

# Get valid keywords from config
valid_keywords = config['valid_keywords']

# Read casts from GptChecked.txt
casts = read_json_from_file('GptChecked.txt')
print(f"Number of casts loaded: {len(casts)}")

# Function to get the most relevant keyword for a given text
def get_most_relevant_keyword(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a specialized JSON data processing assistant. Your task is to add the most relevant keyword to each text to improve classification and information retrieval."},
            {"role": "user", "content": f"Please extract the most relevant keyword from the following text:\n\n{text}"}
        ]
    )
    # Extract and normalize the most relevant keyword from the response
    keyword = response.choices[0].message['content'].strip().strip('"').lower()
    return keyword

# Analyze text, add the most relevant keyword, and filter based on valid keywords
def analyze_and_filter_casts(casts):
    updated_casts = []
    for i, cast in enumerate(casts):
        print(f"Processing cast {i+1}/{len(casts)}")
        try:
            keyword = get_most_relevant_keyword(cast['text'])
            safe_print(keyword)
            cast['keyword'] = keyword
            # Check if the normalized keyword is in the valid keywords list
            if keyword in valid_keywords:
                cast['ManualCheckRelevant'] = "Yes"
            else:
                cast['ManualCheckRelevant'] = "Not"
            updated_casts.append(cast)
        except Exception as e:
            print(f"Error processing cast {i+1}: {e}")
            cast['ManualCheckRelevant'] = "Error"
            updated_casts.append(cast)
    return updated_casts

# Call the function
filtered_casts = analyze_and_filter_casts(casts)

# Print a sample of the filtered data
print("Sample of filtered data (first item):")
safe_print(filtered_casts[:1])

# Write the transformed JSON to a file
output_file = 'ManualChecked.txt'
with codecs.open(output_file, 'w', 'utf-8') as outfile:
    json.dump(filtered_casts, outfile, indent=2, ensure_ascii=False)

print("Manual check completed successfully.")
print(f"Output file size: {os.path.getsize(output_file)} bytes")