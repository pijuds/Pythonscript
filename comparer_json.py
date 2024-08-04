import json
import os
from openpyxl import Workbook


# Load JSON data from files
def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return None

# Get keys from JSON data
def get_keys(json_data, parent_key=''):
    print("parent_key",parent_key)
    keys = set()
    for key, value in json_data.items():
        full_key = f"{parent_key}.{key}" if parent_key else key
        print("full_key",full_key)
        keys.add(full_key)
        if isinstance(value, dict):
            keys.update(get_keys(value, full_key))
    return keys

# Compare keys of two JSON files
def compare_json_keys(file1, file2):
    json1 = load_json(file1)
    json2 = load_json(file2)

    if json1 is None or json2 is None:
        return None, None

    keys1 = get_keys(json1)
    keys2 = get_keys(json2)

    only_in_file1 = keys1 - keys2
    only_in_file2 = keys2 - keys1

    return only_in_file1, only_in_file2

# Main script
def write_keys_to_excel(only_in_file1, only_in_file2, output_file):
    wb = Workbook()
    ws = wb.active
    ws.title = "Extra Keys"

    # Write headers
    ws.append(["Keys only in first file", "Keys only in second file"])

    # Write keys
    max_len = max(len(only_in_file1), len(only_in_file2))
    for i in range(max_len):
        key1 = list(only_in_file1)[i] if i < len(only_in_file1) else ""
        key2 = list(only_in_file2)[i] if i < len(only_in_file2) else ""
        ws.append([key1, key2])

    # Save the Excel file
    wb.save(output_file)
    print(f"Extra keys written to {output_file}")

def main():
    file1 = input("Enter the path for the first JSON file: ")
    file2 = input("Enter the path for the second JSON file: ")

    only_in_file1, only_in_file2 = compare_json_keys(file1, file2)

    if only_in_file1 is not None and only_in_file2 is not None:
        output_file = "extra_keys.xlsx"
        write_keys_to_excel(only_in_file1, only_in_file2, output_file)

if __name__ == "__main__":
    main()