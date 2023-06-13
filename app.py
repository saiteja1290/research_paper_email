from flask import Flask, render_template, request
from openpyxl import Workbook
from openpyxl import load_workbook
from bs4 import BeautifulSoup
import requests
import re
import random

app = Flask(__name__)
def link_to_pdfs_and_titles(domain, subdomain, page = random.randint(1,500)):
    domain = domain.replace(" ", "+")
    subdomain = subdomain.replace(" ", "+")
    titles = []
    titles2 = []
    pdf_links = []
    # url = f"https://link.springer.com/search/page/{page}?facet-language=%22En%22&facet-sub-discipline=%22{subdomain}%22&facet-content-type=%22ConferencePaper%22&sortOrder=newestFirs&facet-discipline=%22{domain}%22"
    # https://link.springer.com/search/page/2?facet-discipline=%22Computer+Science%22&facet-sub-discipline=%22Artificial+Intelligence%22&facet-content-type=%22ConferencePaper%22&facet-language=%22En%22
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
def save_to_excel(name, interests, email, subdomain):
    excel_file = 'registrations.xlsx'
    
    try:
        # Load the existing workbook
        wb = load_workbook(excel_file)
        ws = wb.active
    except FileNotFoundError:
        # If the file doesn't exist, create a new workbook
        wb = Workbook()
        ws = wb.active
        ws['A1'] = 'Name'
        ws['B1'] = 'Interests'
        ws['C1'] = 'Email'
        ws['D1'] = 'subdomain'
    
    ws.append([name, interests, email, subdomain])
    
    wb.save(excel_file)
@app.route("/")
def index():
    return render_template('index.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        interests = request.form['interests']
        email = request.form['email']
        subdomain = request.form['subdomain']

        # Check if any field is empty
        if not name or not interests or not email or not subdomain:
            return '<h2 style="text-align:center">Please fill in all fields.</h2>'

        # Check if the email is in the proper format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return '<h2 style="text-align:center">Invalid email format.</h2>'

        save_to_excel(name, interests, email, subdomain)

        return '<h2 style="text-align:center">Registration successful!</h2>'

    else:
        return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)

