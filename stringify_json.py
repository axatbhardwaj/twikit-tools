import json

def stringify_json():
    # Read the original JSON file
    with open('twikit_cookies.json', 'r') as file:
        data = json.load(file)
    
    # Write the stringified version
    with open('stringified_version.json', 'w') as file:
        json.dump(data, file, separators=(',', ':'))

if __name__ == "__main__":
    stringify_json()