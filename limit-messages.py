import json
from datetime import datetime

def filter_messages_by_date(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    filtered_data = []
    start_date = datetime(2024, 8, 10)
    end_date = datetime(2024, 9, 30, 23, 59, 59)  # Include all of September 30

    for message in data:
        timestamp = datetime.strptime(message['timestamp'], "%Y-%m-%d %H:%M:%S UTC")
        if start_date <= timestamp <= end_date:
            filtered_data.append(message)

    with open(output_file, 'w') as file:
        json.dump(filtered_data, file, indent=2)

    print(f"Filtered {len(filtered_data)} messages from August 10 to September 30, 2024.")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    input_file = "extracted_slack_messages.json"
    output_file = "filtered_messages_aug10_sep30_2024.json"
    filter_messages_by_date(input_file, output_file)