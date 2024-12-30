import json
import os
import sys

def stringify_json(input_path):
    try:
        # Read the original JSON file
        with open(input_path, 'r') as file:
            data = json.load(file)
        
        # Generate output filename in same directory as input
        input_dir = os.path.dirname(input_path)
        input_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(input_dir, f"{input_name}_stringified.json")
        
        # Write the stringified version
        with open(output_path, 'w') as file:
            json.dump(data, file, separators=(',', ':'))
            
        print(f"Stringified JSON saved to: {output_path}")
            
    except FileNotFoundError:
        print(f"Error: File {input_path} not found")
    except json.JSONDecodeError:
        print(f"Error: File {input_path} is not valid JSON")

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else input("Enter the path of the cookies file: ")
    stringify_json(input_file)