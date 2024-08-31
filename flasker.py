from flask import Flask, request, jsonify
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import quote

app = Flask(__name__)

# Function to scrape PDFDrive
def scrape_pdf_drive(query):
    # URL encode the query to handle special characters
    encoded_query = quote(query)
    scraper = cloudscraper.create_scraper()
    url = f"https://www.pdfdrive.com/search?q={encoded_query}"
    
    response = scraper.get(url)
    if response.status_code != 200:
        return []

    # Use html.parser or lxml instead of html5lib to avoid dependency issues
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all('div', class_='file-left')
    
    data = []
    for result in results:
        title = result.find('img')["title"]
        link = result.find('a')["href"].replace("/", "")
        image = result.find('img')["src"]
        data.append({
            'title': title,
            'link': link,
            'image': image
        })
    
    return data

@app.route("/")
def welcome():
    return jsonify({"response": "welcome"})

@app.route("/search")
def search():
    query = request.args.get("book")
    if not query:
        return jsonify({"error": "No search query provided"}), 400

    results = scrape_pdf_drive(query)
    return jsonify({"data": results})

# Run the app
if __name__ == '__main__':
    app.run(debug=False)
