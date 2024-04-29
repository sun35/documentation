from tqdm import tqdm
from trafilatura.sitemaps import sitemap_search
from trafilatura import extract_metadata
import requests
from bs4 import BeautifulSoup

def get_urls_from_site(resource_url: str) -> list:
    # returns urls from a given site
    urls = sitemap_search(resource_url)
    return urls

def create_dataset(list_of_sites):
    print(list_of_sites)
    data = []
    for website in tqdm(list_of_sites, desc="Websites"):
        urls = get_urls_from_site(website)
        for url in tqdm(urls, desc="URLs"):
            try:
                response = requests.get(url)
                response.raise_for_status() #checks for success
                soup = BeautifulSoup(response.content, "html.parser")
                metadata = extract_metadata(response.content)
                title = soup.title.string
                description = metadata.description
                paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
                content = "\n".join(paragraphs)
                d = {
                    "url": url,
                    "title": title,
                    "body": content,
                    "description": description,
                }
                data.append(d)
            except requests.exceptions.HTTPError as exceph:
                print(exceph)
            except requests.exceptions.ConnectionError as errc:
                print(errc)
            except requests.exceptions.Timeout as errt:
                print(errt)
            except requests.RequestException as err:
                print(err)
    print(data)
    print("data printed")
    return data

def scrape(list_of_sites: list) -> None:
    data = create_dataset(list_of_sites)
    print("created dataset")
    with open("./docs/dataset.txt", "w", encoding="utf-8") as file:
        print("create file?")
        for paragraph in data:
            file.write(paragraph["title"] + "\n")
            file.write(paragraph["body"])
    

