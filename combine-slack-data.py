import os
import json
from datetime import datetime
import re

def clean_company_name(name):
    name = name.replace('anon', '').replace('-', ' ')
    name = re.sub(r'\b(new|updated)\b', '', name, flags=re.IGNORECASE)
    name = ' '.join(name.split())
    return name.title().strip()

def extract_text_from_blocks(blocks):
    text = []
    for block in blocks:
        if block['type'] == 'rich_text':
            for element in block.get('elements', []):
                if element['type'] == 'rich_text_section':
                    for item in element.get('elements', []):
                        if item['type'] == 'text':
                            text.append(item['text'])
                        elif item['type'] == 'link':
                            text.append(f"[{item.get('text', item['url'])}]({item['url']})")
    return ' '.join(text)

def extract_message_data(message, company_name):
    msg_type = message.get('type')
    subtype = message.get('subtype')
    
    if msg_type != 'message':
        return None

    text = message.get('text', '')
    user_profile = message.get('user_profile', {})
    user_name = user_profile.get('real_name') or message.get('username') or 'Unknown User'
    
    # Determine if the user is from Anon or the customer
    user_team = user_profile.get('team') or message.get('user_team', '')
    is_anon = 'T05158CD98A' in user_team  # Assuming this is Anon's team ID
    sender_type = 'Anon' if is_anon else 'Customer'
    
    # Format user name with organization
    user_org = 'Anon' if is_anon else company_name
    user_display = f"{user_name} ({user_org})"

    # Handle different subtypes
    if subtype == 'channel_join':
        text = f"User joined the channel: {text}"
    elif subtype == 'message_changed':
        text = message.get('message', {}).get('text', 'Message was edited')
    elif subtype == 'message_deleted' or subtype == 'tombstone':
        text = "This message was deleted."
    elif subtype == 'file_share':
        file_info = message.get('file', {})
        text = f"File shared: {file_info.get('name', 'Unknown file')}. {text}"
    elif subtype == 'bot_message':
        text = f"Bot message: {text}"
        user_display = f"{message.get('username', 'Bot')} (Bot)"
        sender_type = 'Bot'

    # Process rich text and formatted content
    if 'blocks' in message:
        block_text = extract_text_from_blocks(message['blocks'])
        text = f"{text}\n{block_text}".strip()

    # Process attachments
    if 'attachments' in message:
        for attachment in message['attachments']:
            attach_text = attachment.get('text') or attachment.get('fallback', '')
            text += f"\nAttachment: {attach_text}"

    # Handle threaded replies
    if 'thread_ts' in message and message['thread_ts'] != message.get('ts'):
        text = f"Reply in thread: {text}"

    # Convert timestamp to readable format
    ts = float(message.get('ts', 0))
    timestamp = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S UTC')

    return {
        'company': company_name,
        'user': user_display,
        'timestamp': timestamp,
        'message': text.strip(),
        'message_type': subtype or 'regular_message',
        'sender_type': sender_type
    }

def extract_slack_messages(root_directory):
    all_messages = []

    for root, dirs, files in os.walk(root_directory):
        folder_name = os.path.basename(root)
        company_name = clean_company_name(folder_name)
        
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        if isinstance(data, list):
                            for message in data:
                                extracted_message = extract_message_data(message, company_name)
                                if extracted_message:
                                    all_messages.append(extracted_message)
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in file: {file_path}")

    all_messages.sort(key=lambda x: x['timestamp'])

    output_file = 'extracted_slack_messages.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_messages, f, indent=2, ensure_ascii=False)

    print(f"Extracted messages written to {output_file}")

# Usage
root_directory = '/Users/danielmason/Downloads/Anon-slack-export-9.30.24'
extract_slack_messages(root_directory)