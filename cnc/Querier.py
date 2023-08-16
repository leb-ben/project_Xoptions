import requests
import datetime
import re
import sys
import time

# Define variables
query = input("Enter your query: ")
urlscan_api_url = "https://urlscan.io/api/v1/search/?q="
urlscan_api_key = "7175a05e-5816-4482-a742-56d11070c948"                                   
headers = {"Content-type": "application/json", "API-Key": urlscan_api_key}
url_list = []
hex_regex = re.compile(r"\b[a-fA-F0-9]{64}\b")
false_positives = ["f1f1f1", "f0f0f0", "000000", "404", "400", "500", "403", "401"]
matched_strings = set()  # Use a set to automatically eliminate duplicates
time_limit = datetime.timedelta(minutes=4)
start_time = datetime.datetime.now()
delay_time = 0.01  # seconds

# Perform initial API search on urlscan.io
urlscan_query = f"{query}"
urlscan_api_url = f"https://urlscan.io/api/v1/search/?q={urlscan_query}"
while True:
    resp = requests.get(urlscan_api_url, headers=headers)
    if resp.ok:
        break
    elif resp.status_code == 429:
        reset_time = int(resp.headers.get("X-Retry-After", f"{delay_time}"))
        print(f"Rate limit exceeded. Waiting {reset_time} seconds before retrying...")
        time.sleep(reset_time)
    else:
        print(f"Error: Could not retrieve URL scan results. Status code: {resp.status_code}.")
        print(resp.json().get("message"))
        sys.exit()

# Parse URL list from API response
results = resp.json().get("results", [])
url_list = [r.get("page").get("url") for r in results]

# Search for hex strings in each URL
for url in url_list:
    # Send HTTP request
    try:
        resp = requests.get(url)
    except requests.exceptions.RequestException:
        continue

    # Search for hex strings
    matched = hex_regex.findall(resp.text)
    for s in matched:
        if s not in false_positives:
            matched_strings.add(s)

    # Check if enough matches were found
    if len(matched_strings) >= 100:
        break

    # Add delay between API requests
    time.sleep(delay_time)

    # Check if time limit has been reached
    if (datetime.datetime.now() - start_time) >= time_limit:
        break

# Write unique hex strings to file
with open("keys.txt", "w") as keys_file:  # Open the file in write mode
    for s in matched_strings:
        keys_file.write('0x' + s + "\n")

# Output matched hex strings
if len(matched_strings) == 0:
    print(f"No matched hex strings found for query '{query}'")
else:
    print(f"Found {len(matched_strings)} matched hex strings:")
    for s in matched_strings:
        print('0x' + s)
