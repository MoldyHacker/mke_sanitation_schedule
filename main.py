import requests
from bs4 import BeautifulSoup

# City of Milwaukee Garbage and Recycling Collection Schedule
# https://itmdapps.milwaukee.gov/DpwServletsPublic/garbage_day

# Define the URL and parameters
url = "https://itmdapps.milwaukee.gov/DpwServletsPublic/garbage_day"
data = {
    "laddr": "200",
    "sdir": "E",
    "sname": "WELLS",
    "stype": "ST"
}

garbage_pickup_string = "Next Scheduled Garbage Pickup:"
recycling_pickup_string = "Next Scheduled Recycling Pickup:"

try:
    # Send the POST request
    response = requests.post(url, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        # print("Response received successfully!")

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract relevant data
        # address = soup.find('h1').string.strip() if soup.find('h1') else "Address not found"  # Always returns "Address located!"
        if soup.find('h2', string="Next Scheduled Garbage Pickup:"):
            # Locate the header with the desired text
            garbage_header = soup.find('h2', string=garbage_pickup_string)
            # Find all <strong> tags following the header
            garbage_strong_tags = garbage_header.find_all_next('strong', limit=2)
            next_garbage_pickup = garbage_strong_tags[1].get_text(strip=True) if len(garbage_strong_tags) >= 2 else "Garbage pickup date not found"

            # Locate the header with the desired text
            recycling_header = soup.find('h2', string=recycling_pickup_string)
            # Find all <strong> tags following the header
            recycling_strong_tags = recycling_header.find_all_next('strong', limit=2)
            next_recycling_pickup = recycling_strong_tags[1].get_text(strip=True) if len(recycling_strong_tags) >= 2 else "Recycling pickup date not found"

            # Print the extracted data
            print(f"Next Garbage Pickup: {next_garbage_pickup}")
            print(f"Next Recycling Pickup: {next_recycling_pickup}")
        else:
            print("Unable to locate the address.")
    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
