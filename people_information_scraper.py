import pandas as pd
from bs4 import BeautifulSoup
import requests
import openpyxl

# Read the links from the text file
with open('speaker_links.txt', 'r') as file:
    links = file.readlines()

# Header for the request
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

# Initialize a list to store the scraped data
data = []

# Loop through each speaker link and scrape information
for link in links:
    link = link.strip()  # Clean up any extra spaces or newlines
    
    response = requests.get(link, headers=headers)
    response.raise_for_status()  # Ensure the request was successful
    
    web_page = response.text
    soup = BeautifulSoup(web_page, 'html.parser')
    
    # Extract speaker details
    try:
        name = soup.find('h1', class_='headlines__H1-sc-31df2319-0 hUYlOC').getText(strip=True)
    except AttributeError:
        name = 'N/A'
    
    try:
        tags = soup.find_all('h2', class_='headlines__SubHeading-sc-31df2319-6 kmQWph')
        function = tags[0].text.strip() if len(tags) > 0 else 'N/A'
        company = tags[1].text.strip() if len(tags) > 1 else 'N/A'
    except (AttributeError, IndexError):
        function = 'N/A'
        company = 'N/A'

    try:
        bio = soup.find('div', class_='ProfileDetails__ProfileDetailsContent-sc-8beaea78-1 jmHeNd').getText(strip=True)
    except AttributeError:
        bio = 'N/A'
    
    try:
        tags_2 = soup.find_all('p', class_='bodyCopy__P-sc-986c63f9-1 eucMHK')
        location = tags_2[0].text.strip() if len(tags_2) > 0 else 'N/A'
        industry = tags_2[1].text.strip() if len(tags_2) > 1 else 'N/A'
    except (AttributeError, IndexError):
        location = 'N/A'
        industry = 'N/A'
    
    
    
    # Append the data to the list
    data.append({
        'Name': name,
        'Function': function,
        'Company': company,
        'Description': bio,
        'Location': location,
        'Industry': industry,
    })

    # Save the data incrementally after every few profiles
    if len(data) % 10 == 0:  # Save every 10 profiles
        df = pd.DataFrame(data)
        with pd.ExcelWriter('speakers.xlsx', engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, index=False, header=writer.sheets == {})

# Final save for any remaining profiles
df = pd.DataFrame(data)
df.to_excel('speakers.xlsx', index=False)
print("Data has been successfully saved to 'speakers.xlsx'.")
