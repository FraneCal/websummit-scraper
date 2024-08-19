import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd

# Read the links from the text file
with open('links_startups.txt', 'r') as file:
    links = [link.strip() for link in file.readlines()]

# Header for the request
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

# Asynchronous function to fetch a webpage
async def fetch(session, url):
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

# Function to parse the data from a webpage
def parse(web_page):
    soup = BeautifulSoup(web_page, 'html.parser')
    
    try:
        name = soup.find('h1', class_='headlines__H1-sc-31df2319-0 hUYlOC').getText(strip=True)
    except AttributeError:
        name = 'N/A'
    
    try:
        description = soup.find('div', class_='ProfileDetails__ProfileDetailsContent-sc-8beaea78-1 jmHeNd').getText(strip=True)
    except AttributeError:
        description = 'N/A'
    
    try:
        tags = soup.find_all('p', class_='bodyCopy__P-sc-986c63f9-1 eucMHK')
        location = tags[0].text.strip() if len(tags) > 0 else 'N/A'
        industry = tags[1].text.strip() if len(tags) > 1 else 'N/A'
    except (AttributeError, IndexError):
        location = 'N/A'
        industry = 'N/A'
    
    try:
        website = soup.find('a', class_='Button__StyledButton-sc-d4ee7b0f-0 SocialButton__SocialButtonEL-sc-29e85cc1-1 hnAnPe dmxDbr').get('href', 'N/A')
    except AttributeError:
        website = 'N/A'
    
    return {
        'Name': name,
        'Description': description,
        'Location': location,
        'Industry': industry,
        'Website': website
    }

# Asynchronous main function to handle fetching and processing links
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        data = []
        
        for link in links:
            tasks.append(fetch(session, link))
        
        # Fetch pages asynchronously
        pages = await asyncio.gather(*tasks)
        
        for page in pages:
            if page:
                data.append(parse(page))
        
        # Convert the data to a DataFrame
        df = pd.DataFrame(data)
        
        # Save the DataFrame to an Excel file
        df.to_csv('startups.csv', index=False)
        print("Data has been successfully saved to 'startups.csv'.")

# Run the asynchronous main function
if __name__ == '__main__':
    asyncio.run(main())
