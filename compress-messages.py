import json

def compress_messages(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    compressed_data = []
    for item in data:
        # Skip channel_join messages, messages from "Bot (Bot)", and messages from Anon
        if (item['message_type'] == 'channel_join' or 
            item['user'] == 'Bot (Bot)' or 
            item['sender_type'] == 'Anon'):
            continue
        
        compressed_item = {
            'c': item['company'],
            'u': item['user'],
            't': item['timestamp'],
            'm': item['message']
        }
        compressed_data.append(compressed_item)

    # Remove any indentation and newlines from the JSON output
    compressed_json = json.dumps(compressed_data, separators=(',', ':'))

    with open(output_file, 'w') as f:
        f.write(compressed_json)

    print(f"Compressed data saved to {output_file}")

# Usage
input_file = 'filtered_messages_aug10_sep30_2024.json'
output_file = 'compressed_slack_messages.json'
compress_messages(input_file, output_file)