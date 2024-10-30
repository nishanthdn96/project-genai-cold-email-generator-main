import csv
import re

# File paths
input_file_path = 'chat.txt'  # Path to your input text file
output_file_path = 'output.csv'  # Path to save the output CSV

# Initialize an empty list to hold processed messages
messages = []

# Define a regex pattern to match lines that start with a timestamp (e.g., '8/23/24, 7:50-PM')
timestamp_pattern = re.compile(r'^\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}-[APM]+ - ')

# Variables to accumulate message data
current_message = None

# Read the file
with open(input_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        # Check if the line starts with a timestamp
        if timestamp_pattern.match(line):
            # Save the current message if it exists
            if current_message:
                messages.append(current_message)
            # Reset and start a new message
            timestamp, message = line.split(" - ", 1)
            # Split by ": " to get sender and content if possible
            if ": " in message:
                sender, content = message.split(": ", 1)
            else:
                sender, content = message, ""  # Handle cases without content
            current_message = [timestamp, sender, content]
        else:
            # Append continuation lines to the current message content
            if current_message:
                current_message[2] += " " + line

    # Append the last message if it exists
    if current_message:
        messages.append(current_message)

# Remove any messages with "<Media omitted>" or "This message was deleted" in the content
messages = [msg for msg in messages if "<Media omitted>" not in msg[2] and "This message was" not in msg[2]]

# Write to CSV
with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    writer.writerow(["Timestamp", "Sender", "Message"])
    # Write rows
    writer.writerows(messages)

print(f"Data has been written to {output_file_path}")
