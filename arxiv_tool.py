#step 1:  Access arXiv using URL.
import requests
def search_arxiv_papers(topic:str, max_results:int = 5)->dict:
    """
    Function to search arXiv using a query and return the results.
    """
    # Prompt user for input
    query = "+".join(topic.lower().split())
    for char in list("!@#$%^&*()_={}[]|\\:;\"'<>,.?/"):
        if char in query:
            print(f"Invalid character {char} in query {query}")
            raise ValueError(f"Invalid character {char} in query {query}")

# Construct the URL for the API request
    url = (
        "https://export.arxiv.org/api/query"
        f"?search_query=all:{query}"
        f"&max_results={max_results}"
        "&sort_by=submittedDate"
        "&sort_order=descending"
    )
    print(f"Making request to URL: {url}")

    # Make the GET request to the arXiv API
    response = requests.get(url)


    if response.status_code != 200:
        print(f"ArXiv API request failed {response.status_code}")
        raise ValueError(f"ArXiv API request failed with status code {response.status_code}")

    #data = parse_arxiv_xml(response.text)
    return response.text


import xml.etree.ElementTree as ET
def parse_arxiv_xml(xml_data: str) -> dict:
    """
    Function to parse the XML data returned by the arXiv API.
    """
    root = ET.fromstring(xml_data)

    enteries = []
    
    ns = {
        'atom': 'http://www.w3.org/2005/Atom',
        'arxiv': 'http://arxiv.org/schemas/atom'
        }

    for entry in root.findall('atom:entry', ns):
        #Extract authors
        authors = [
            authors.find_text('atom:name', ns)
            for authors in entry.findall('atom:author', ns)           
        ]
        # Extract categories from term attribute
        categories = [
            category.get('term')
            for category in entry.findall('atom:category', ns)
        ]
        # Extract PDF link (rel="related" and  type ="application/pdf" )
        pdf_link = None
        
        for link in entry.findall('atom:link', ns):
            if link.get('rel') == 'related' and link.get('type') == 'application/pdf':
                pdf_link = link.atrrib.get('href')
                break
        enteries.append({
            'title': entry.findtext('atom:title', ns),
            "summary": entry.findtext('atom:summary', ns),
            'authors': authors,
            'categories': categories,
            'pdf_link': pdf_link
        })

#convvert the function to a tool
@tool
def arxiv_search(topic: str) -> list[dict]:
    """ Search arXiv for papers on a given topic and return a list of dictionaries with paper details.
    Args:
        topic (str): The topic to search for.
    Returns:
        list[dict]: A list of dictionaries containing paper details.
    """
    papers = search_arxiv_papers(topic)
    return parse_arxiv_xml(papers)

