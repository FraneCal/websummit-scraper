from bs4 import BeautifulSoup
import requests

BASE_URL = 'https://websummit.com/speakers/page/'

# Header for the request
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

all_links = []

# Loop through all 5 pages
for page in range(1, 6):
    # Construct the URL for each page
    url = f'{BASE_URL}{page}/'
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Ensure the request was successful
    
    web_page = response.text
    soup = BeautifulSoup(web_page, 'html.parser')
    
    # Locate the section containing speaker links
    speaker_section = soup.find('div', class_='AttendeeList__AttendeeListGridWrapper-sc-99167293-2 hiqlA-D')
    
    # Find all links within that section
    if speaker_section:
        links = speaker_section.find_all('a', href=True)
        
        # Extract and save each link
        for link in links:
            href = link.get('href')
            full_link = f'https://websummit.com{href}'
            all_links.append(full_link)

# Save all links into a txt file
with open('speaker_links.txt', 'w') as file:
    for link in all_links:
        file.write(f"{link}\n")

print(f"Total number of links: {len(all_links)}")
print("Links saved to speaker_links.txt")
