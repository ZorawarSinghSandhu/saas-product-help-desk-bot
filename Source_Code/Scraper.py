from bs4 import BeautifulSoup
import requests
import re

url = "https://cal.com/help/welcome"

while True:
    response = requests.get(url)
    if response.status_code == 200:
        if "help/" not in response.url:
            break
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.find(id = "page-title")
        title = title.get_text(strip = True)
        
        file_name = title.strip().lower().replace(" ", "_")
        
        file_name = re.sub(r'[\\/*?":;<>|]', '_', file_name)
        
        with open("../Raw_text/" + file_name + ".txt", mode="w", newline='', encoding='utf-8') as f:
            header = soup.find(id = "header")
            content = soup.find(id = "content")
            f.write("\n\n")
            f.write(header.get_text(separator = "\n", strip = True))
            f.write("\n")
            f.write(content.get_text(separator = "\n", strip = True))
        
        pagination = soup.find(id = "pagination")
        href = pagination.find("a", class_="ml-auto")["href"]
        url = "https://cal.com" + href
        
    else:
        print(f"Extraction Failed! Currently at URL:\n{url}\n")
        

        
        
        
    

