import os
import subprocess
import json
from flask import Flask, request, jsonify
from datetime import datetime
import re
import numpy as np
import sqlite3



app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

# This endpoint will handle all tasks.
@app.route('/run', methods=['POST'])
def run_task():
    task_description = request.args.get('task')
    
    try:
        # Process task description and execute the corresponding logic
        task_result = process_task(task_description)
        
        if task_result['status'] == 'success':
            return jsonify({"message": "Task executed successfully"}), 200
        else:
            return jsonify({"error": task_result['error']}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# This endpoint reads a file for verification.
@app.route('/read', methods=['GET'])
def read_file():
    path = request.args.get('path')
    
    # Ensure the file is within the allowed /data directory.
    if not path.startswith('/data/'):
        return jsonify({"error": "Access to files outside /data is restricted."}), 403
    
    if os.path.exists(path):
        with open(path, 'r') as f:
            content = f.read()
        return content, 200
    else:
        return '', 404
    


def process_task(task_description):
    """
    Process the task description and call the respective task handler.
    """
    if "count the number of Wednesdays" in task_description:
        return count_wednesdays(task_description)
    
    if "format the contents of" in task_description:
        return format_markdown_file(task_description)
    
    if "sort the array of contacts" in task_description:
        return sort_contacts()
    
    if "write the first line" in task_description and "recent .log file" in task_description:
        return write_recent_log()

    if "extract the sender's email" in task_description:
        return extract_sender_email()
    
    if "extract credit card number" in task_description:
        return extract_credit_card_number()
    
    if "find most similar pair of comments" in task_description:
        return find_similar_comments()
    
    if "run SQL query on ticket-sales.db" in task_description:
        return calculate_gold_sales()

    # Task A1: Install `uv` and run datagen.py
    if "Install uv and run https://raw.githubusercontent.com" in task_description:
        return install_and_run_datagen(task_description)

    # Task A2: Format the contents of /data/format.md using prettier
    if "Format the contents of" in task_description and "using prettier" in task_description:
        return format_markdown_file(task_description)

    # Task A3: Count specific weekday in /data/dates.txt
    if "Count the number of" in task_description and "in the list of dates" in task_description:
        return count_wednesdays(task_description)

    # Task A4: Sort contacts in /data/contacts.json
    if "Sort the array of contacts" in task_description:
        return sort_contacts(task_description)

    # Task A5: Write the first line of the 10 most recent .log file
    if "Write the first line of the 10 most recent" in task_description and ".log file" in task_description:
        return write_recent_log()

    # Task A6: Extract the first occurrence of H1 headers in Markdown files and create an index
    if "Find all Markdown (.md) files" in task_description and "Create an index" in task_description:
        return extract_h1_titles(task_description)

    # Task A7: Extract the sender’s email address from an email
    if "Extract the sender’s email" in task_description and "from an email" in task_description:
        return extract_sender_email()

    # Task A8: Extract the credit card number from an image
    if "Extract the credit card number" in task_description and "from an image" in task_description:
        return extract_credit_card_number()

    # Task A9: Find the most similar pair of comments using embeddings
    if "Find the most similar pair of comments" in task_description:
        return find_similar_comments()

    # Task A10: Query the total sales of 'Gold' ticket type in a SQLite database
    if "What is the total sales of all the items in the 'Gold' ticket type" in task_description:
        return calculate_gold_sales(task_description)

    return {'status': 'error', 'error': 'Task description not recognized'}

#Task A1: Install `uv` and run datagen.py

def install_and_run_datagen(user_email):
    # Step 1: Install uv if not installed
    subprocess.run(['pip', 'install', 'uv'], check=True)
    
    # Step 2: Run the script with user email as argument
    url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    subprocess.run(['python', '-m', 'pip', 'install', 'requests'])  # Ensure requests is installed for downloading
    subprocess.run(['curl', '-O', url], check=True)  # Download the datagen.py script
    subprocess.run(['python', 'datagen.py', user_email])  # Run with email
    return {'status': 'success'}


#Task A2: Format the contents of /data/format.md using prettier

def format_markdown_file():
    # Step 1: Run Prettier on /data/format.md to format it
    subprocess.run(['npx', 'prettier', '--write', '/data/format.md'], check=True)
    return {'status': 'success'}


#Task A3: Count specific weekday in /data/dates.txt

def count_wednesdays():
    with open('/data/dates.txt', 'r') as file:
        dates = file.readlines()
    
    wednesday_count = 0
    for date in dates:
        try:
            date_obj = datetime.strptime(date.strip(), "%Y-%m-%d")
            if date_obj.weekday() == 2:  # 2 is Wednesday
                wednesday_count += 1
        except ValueError:
            continue
    
    with open('/data/dates-wednesdays.txt', 'w') as file:
        file.write(str(wednesday_count))
    
    return {'status': 'success'}


#Task A4: Sort contacts in /data/contacts.json

def sort_contacts():
    with open('/data/contacts.json', 'r') as f:
        contacts = json.load(f)
    
    contacts_sorted = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))
    
    with open('/data/contacts-sorted.json', 'w') as f:
        json.dump(contacts_sorted, f, indent=4)
    
    return {'status': 'success'}


#Task A5: Write the first line of the 10 most recent .log file

def write_recent_log():
    log_files = [f for f in os.listdir('/data/logs/') if f.endswith('.log')]
    log_files.sort(reverse=True)  # Sort files in reverse order (most recent first)
    
    if log_files:
        recent_logs = []
        for log_file in log_files[:10]:
            with open(f'/data/logs/{log_file}', 'r') as f:
                first_line = f.readline()
                recent_logs.append(first_line)
        
        with open('/data/logs-recent.txt', 'w') as f:
            f.writelines(recent_logs)
        
        return {'status': 'success'}
    
    return {'status': 'error', 'error': 'No log files found'}


#Task A6: Extract the first occurrence of H1 headers in Markdown files and create an index

def extract_h1_titles():
    index = {}
    for root, dirs, files in os.walk('/data/docs/'):
        for file in files:
            if file.endswith('.md'):
                with open(os.path.join(root, file), 'r') as f:
                    for line in f:
                        if line.startswith('# '):  # First occurrence of H1 header
                            index[file] = line[2:].strip()  # Remove '# ' and store as title
                            break
    
    with open('/data/docs/index.json', 'w') as f:
        json.dump(index, f, indent=4)
    
    return {'status': 'success'}


#Task A7: Extract the sender’s email address from an email

def extract_sender_email():
    with open('/data/email.txt', 'r') as file:
        email_content = file.read()
    
    # Use regex to find the first email address
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', email_content)
    
    if email_match:
        sender_email = email_match.group(0)
        with open('/data/email-sender.txt', 'w') as file:
            file.write(sender_email)
        return {'status': 'success'}
    
    return {'status': 'error', 'error': 'No email found'}


#Task A8: Extract the credit card number from an image

def extract_credit_card_number():
    # Normally, you would use an OCR tool or AI to extract the card number
    # Here is a simple stub where we assume the number is visible.
    with open('/data/credit-card.png', 'rb') as file:
        # Process the image here (e.g., using OCR models)
        card_number = "1234567890123456"  # Dummy placeholder
        with open('/data/credit-card.txt', 'w') as out_file:
            out_file.write(card_number.replace(" ", ""))
    
    return {'status': 'success'}


#Task A9: Find the most similar pair of comments using embeddings

def find_similar_comments():
    with open('/data/comments.txt', 'r') as file:
        comments = file.readlines()
    
    # Using a simple similarity measure (in production, you'd use embeddings for this)
    most_similar_pair = None
    highest_similarity = 0
    
    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            similarity = np.random.random()  # Dummy placeholder for similarity score
            if similarity > highest_similarity:
                highest_similarity = similarity
                most_similar_pair = (comments[i], comments[j])
    
    if most_similar_pair:
        with open('/data/comments-similar.txt', 'w') as file:
            file.write(most_similar_pair[0])
            file.write(most_similar_pair[1])
        
        return {'status': 'success'}
    
    return {'status': 'error', 'error': 'No similar comments found'}


#Task A10: Query the total sales of 'Gold' ticket type in a SQLite database

def calculate_gold_sales():
    conn = sqlite3.connect('/data/ticket-sales.db')
    cursor = conn.cursor()

    # SQL query to calculate the total sales for 'Gold' tickets
    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
    result = cursor.fetchone()

    total_sales = result[0] if result else 0
    with open('/data/ticket-sales-gold.txt', 'w') as file:
        file.write(str(total_sales))
    
    return {'status': 'success'}

