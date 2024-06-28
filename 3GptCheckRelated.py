import openai
import json
import codecs
import os
import sys
from backoff import on_exception, expo
from openai.error import RateLimitError

def safe_print(obj):
    try:
        print(json.dumps(obj, indent=2, ensure_ascii=False))
    except UnicodeEncodeError:
        print(json.dumps(obj, indent=2, ensure_ascii=True))

# Read configuration from config.json
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

# Read casts from transformed_json.txt
casts = read_json_from_file('transformed_json.txt')
print(f"Number of casts loaded: {len(casts)}")

# Process each cast entry
for i, cast in enumerate(casts):
    print(f"Processing cast {i+1}/{len(casts)}")
    prompt = f"Does the text: \"{cast['text']}\" contain related information in the keywords: {', '.join(valid_keywords)}?'Yes' means that the text is related to the keywords. 'No' means that the text is not related to the keywords at all."
    @on_exception(expo, RateLimitError, max_tries=5)
    def process_cast():
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Determine the relevance of the keywords in the text."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50
        )
        return response

    try:
        response = process_cast()
        print(response['choices'][0]['message']['content']+"\n--------")
        
        # Determine relevance based on model response
        relevance = "Not" if "no" in response['choices'][0]['message']['content'].lower() else "Yes"
        cast['OpenAICheckRelevant'] = relevance
    except Exception as e:
        print(f"Error processing cast {i+1}: {e}")
        cast['OpenAICheckRelevant'] = "Error"

# Print updated JSON
print("Sample of processed data (first item):")
safe_print(casts[:1])

# Write the transformed JSON to a file
with codecs.open('GptChecked.txt', 'w', 'utf-8') as outfile:
    json.dump(casts, outfile, indent=2, ensure_ascii=False)

print("GPT check completed successfully.")
print(f"Output file size: {os.path.getsize('GptChecked.txt')} bytes")