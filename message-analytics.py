import json
from collections import Counter

def analyze_slack_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    total_messages = len(data)
    message_types = Counter()
    companies = Counter()
    users = Counter()

    for message in data:
        message_types[message['message_type']] += 1
        companies[message['company']] += 1
        users[message['user']] += 1

    print(f"Total messages: {total_messages}")

    print("\nMessages by type:")
    for message_type, count in message_types.items():
        print(f"{message_type}: {count}")

    print("\nMessages by company:")
    for company, count in companies.most_common():
        print(f"{company}: {count}")

    print("\nMessages by user:")
    for user, count in users.most_common():
        print(f"{user}: {count}")

if __name__ == "__main__":
    file_path = "extracted_slack_messages.json"  # Update this if your file has a different name
    analyze_slack_data(file_path)