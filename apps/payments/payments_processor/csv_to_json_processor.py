import csv
import json

def csv_to_json(csv_file):
    """
    Reads a CSV file and transforms it into a JSON object.

    Parameters:
    - csv_path: str, the path to the CSV file

    Returns:
    - json_data: dict, the JSON object created from the CSV data
    """
    file_content = csv_file.read()
    
    # Now you can use file_content as bytes
    # For example, you can save it to a file on disk
    with open('bank_statement.csv', 'wb') as destination_file:
        destination_file.write(file_content)

    
    # Open the CSV file
    with open('bank_statement.csv', "r") as csv_file:
        # Read the CSV data
        csv_data = csv.DictReader(csv_file)

        # Create an empty list to store the CSV rows
        rows = []

        # Loop through each row of the CSV data
        for row in csv_data:
            # Add the row to the list
            rows.append(row)

    # Convert the list of rows to a JSON object
    json_data = json.dumps(rows)

    # Return the JSON object
    return json_data
    