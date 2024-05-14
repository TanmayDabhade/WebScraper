from bs4 import BeautifulSoup as BS
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='FrontEnd')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrapePage():
    '''
    Scrape a webpage and extract specified elements' attributes.

    This function handles POST requests to the '/scrape' route. It accepts two form parameters:
    - 'url': The URL of the webpage to scrape.
    - 'element': The HTML element to extract from the webpage.

    The function performs the following actions:
    1. Retrieves the URL and element type from the form data.
    2. Sends a GET request to the provided URL to fetch the webpage content.
    3. Parses the webpage content using BeautifulSoup.
    4. Finds all instances of the specified HTML element in the webpage.
    5. Extracts and collects the attributes of these elements.
    6. Renders an HTML template ('attributes.html') with the extracted attributes.

    If no elements of the specified type are found, it returns a message indicating no elements were found.

    Returns:
        A rendered HTML template displaying the attributes of the specified elements, or a message if no elements are found.
    '''
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
    '''
    Scrapes a web page for specific HTML elements and retrieves the values of a specified attribute.

    This function is triggered by a POST request containing a URL, an HTML element to search for, and 
    an attribute to retrieve from the elements. It sends a GET request to the specified URL, parses the 
    HTML content, and finds all occurrences of the specified element. It then extracts the values of the 
    specified attribute from each element and renders a template displaying these values.

    Returns:
        A rendered HTML template displaying the values of the specified attribute for the found elements.

    Request form parameters:
        url (str): The URL of the web page to scrape.
        element (str): The HTML element to search for in the web page.
        attribute (str): The attribute whose values need to be retrieved from the found elements.

    Renders:
        results.html: A template that displays the values of the specified attribute for the found elements.

    Example:
        Sending a POST request with 'url' set to 'http://example.com', 'element' set to 'a', and 
        'attribute' set to 'href' will scrape 'http://example.com' for all <a> tags and display their 'href' attribute values.

    '''
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
