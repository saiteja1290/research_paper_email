from bs4 import BeautifulSoup
import requests
import re
import random

def link_to_pdfs_and_titles(domain, subdomain, page = random.randint(1,500)):
    domain = domain.replace(" ", "+")
    subdomain = subdomain.replace(" ", "+")
    titles = []
    titles2 = []
    pdf_links = []
    url = f"https://link.springer.com/search/page/{page}?facet-language=%22En%22&showAll=false&facet-content-type=%22ConferencePaper%22&facet-sub-discipline=%22{subdomain}%22&facet-discipline=%22{domain}%22"

    response = requests.get(url)
    html_content = response.content


    soup = BeautifulSoup(html_content, "html.parser")


    target_links = soup.find_all("a", class_="webtrekk-track pdf-link")
    # target_links_title = soup.find_all("a", class_="title")
    for link in target_links:
        if(link.get("doi")):    
            # titles = link.text
            href = link.get("doi")
            title = link.get("aria-label")
            pdf_links.append("https://link.springer.com//content/pdf/"+href)
            titles.append(title)
    print(pdf_links)
    # print(title)
    for title in titles:
        modified_text = re.sub(r"Download PDF \(\d+ KB\) - ", "", title)
        # title = modified_text
        titles2.append(modified_text)
    print(titles2)

    file_path = "text.txt"  # Replace with the desired file path

# Open the file in write mode
    with open(file_path, "w") as file:
        for i in range(min(len(titles2), len(pdf_links))):
            file.write(titles2[i].replace('\xa0', '') + ": "+ pdf_links[i]+"\n\n")


link_to_pdfs_and_titles("Computer Science", "Artificial Intelligence", 2)