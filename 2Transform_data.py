import json
import codecs
import os
import sys

def safe_print(obj):
    try:
        print(json.dumps(obj, indent=2, ensure_ascii=False))
    except UnicodeEncodeError:
        print(json.dumps(obj, indent=2, ensure_ascii=True))

def read_json_from_file(file_path):
    print(f"Attempting to read file: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    print(f"File size: {os.path.getsize(file_path)} bytes")

    encodings_to_try = ['utf-8', 'iso-8859-1']
    
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

def transform_data(original_json):
    new_json = []
    for item in original_json:
        cast = item['cast']
        print(f"Cast: {cast['hash']}")
        text = cast['text']
        new_item = {
            "hash": cast['hash'],
            "username": cast['castedBy']['fnames'][0] if cast['castedBy'] is not None else None,
            "fid": cast['fid'],
            "text": text,
            "channel": cast['channel']['name'] if cast['channel'] else None,
            "likes": cast['numberOfLikes'],
            "recasts": cast['numberOfRecasts'],
            "replies": cast['numberOfReplies'],
            "scv": cast['socialCapitalValue']['formattedValue'],
            "tags": cast['channel']['name'] if cast['channel'] else None,
            "casted_at": cast['castedAtTimestamp'],
        }
        new_json.append(new_item)
    return new_json

file_path = 'AllTrendOutput.txt'

try:
    original_json = read_json_from_file(file_path)
    print(f"Successfully loaded JSON data. Number of items: {len(original_json)}")
except Exception as e:
    print(f"Error reading file: {e}")
    print("File content (first 1000 characters):")
    with open(file_path, 'rb') as file:
        print(file.read(1000))
    raise

transformed_json = transform_data(original_json)
print(f"Transformation completed. Number of transformed items: {len(transformed_json)}")

print("Sample of transformed JSON (first item):")
safe_print(transformed_json[:1])

output_file = 'transformed_json.txt'
with codecs.open(output_file, 'w', 'utf-8') as outfile:
    json.dump(transformed_json, outfile, indent=2, ensure_ascii=False)

print(f"Transformation completed successfully. Output written to {output_file}")
print(f"Output file size: {os.path.getsize(output_file)} bytes")