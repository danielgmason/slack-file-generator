# Slack Message Extractor

This project provides a Python script to extract and combine messages from a Slack workspace export into a single, easy-to-read JSON file. It's designed to capture various types of messages, including regular messages, channel joins, edited messages, deleted messages, file shares, and bot messages, while also distinguishing between messages from your company (Anon) and customer companies.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [How to Export Slack Data](#how-to-export-slack-data)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Output Format](#output-format)
6. [Customization](#customization)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.6 or higher
- Access to export data from your Slack workspace (admin privileges may be required)

## How to Export Slack Data

To export data from your Slack workspace:

1. Go to your Slack workspace in a web browser.
2. Click on the workspace name in the top left to open the menu.
3. Select "Settings & administration" > "Workspace settings".
4. In the menu on the left, click on "Import/Export Data".
5. In the "Export" tab, click on "Start Export".
6. Choose the date range and types of data you want to export.
7. Click "Start Export".
8. Wait for the export to complete. You'll receive an email when it's ready.
9. Download the export file (it will be a zip file).

Note: The exact steps and available options may vary depending on your Slack plan and admin settings.

## Installation

1. Clone this repository or download the script file:
   ```
   git clone https://github.com/yourusername/slack-message-extractor.git
   ```
   or download `extract_slack_messages.py` directly.

2. Navigate to the project directory:
   ```
   cd slack-message-extractor
   ```

3. No additional libraries are required as the script uses only Python standard libraries.

## Usage

1. Extract the Slack export zip file you downloaded.

2. Open the `extract_slack_messages.py` file and update the `root_directory` variable at the bottom of the script with the path to your extracted Slack data:
   ```python
   root_directory = '/path/to/your/slack/export/directory'
   ```

3. Run the script:
   ```
   python extract_slack_messages.py
   ```

4. The script will process all JSON files in the specified directory and its subdirectories, and create a file named `extracted_slack_messages.json` in the same directory as the script.

## Output Format

The output JSON file will contain an array of message objects. Each message object includes:

- `company`: The name of the customer company (derived from the folder name)
- `user`: The name of the user who sent the message, including their organization in parentheses
- `timestamp`: The time the message was sent (in UTC)
- `message`: The content of the message
- `message_type`: The type of message (e.g., regular_message, channel_join, file_share)
- `sender_type`: Whether the sender is from Anon, a Customer, or a Bot

## Customization

- To change the Anon team identifier, modify the `is_anon` check in the `extract_message_data` function:
  ```python
  is_anon = 'T05158CD98A' in user_team  # Replace with your Anon team ID
  ```

- To modify how company names are cleaned, adjust the `clean_company_name` function.

## Troubleshooting

- If you encounter a `JSONDecodeError`, check that your Slack export files are valid JSON.
- If certain messages are missing, ensure that the export includes all the channels and message types you need.
- For large exports, the script may take some time to run. Be patient and ensure your computer doesn't go to sleep during processing.

For any other issues or feature requests, please open an issue on the GitHub repository.