from bs4 import BeautifulSoup as BS
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='FrontEnd')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrapePage():
    ''''''
    link = request.form['url']
    element_to_extract = request.form['element']
    page = requests.get(link)
    soup = BS(page.content, 'html.parser')
    extracted_elements = soup.find_all(element_to_extract)
    if not extracted_elements:
        return 'No elements found'
    attributes = set()
    for element in extracted_elements:
        a = element.attrs
        attributes.update(a.keys())
    return render_template('attributes.html', attributes=attributes, url=link, element=element_to_extract)

@app.route('/choose', methods=['POST'])
def getAttributes():
    '''This function is the scraping script, which manages the'''
    attribute = request.form['attribute']
    link = request.form['url']
    elements_to_extract = request.form['element']

    page = requests.get(link)
    soup = BS(page.content, 'html.parser')

    elements = soup.find_all(elements_to_extract)
    results = [el.get(attribute, 'N/A') for el in elements]

    return render_template('results.html', attribute=attribute, results=results)

if __name__ == '__main__':
    app.run(debug=True)
