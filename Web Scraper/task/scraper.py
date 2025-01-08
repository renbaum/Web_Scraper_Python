import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    print("Input the URL:")
    url = input()
    # url = "https://www.nature.com/articles/d41586-023-00103-3"

    try:
        if "nature.com" not in url: raise Exception("Invalid page!")
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        if(response.status_code != 200):
            raise Exception("Invalid page!")
        soup = BeautifulSoup(response.text, 'html.parser')
        titel = soup.find('title')
        title = titel.text
        description = soup.find('meta', attrs={"name": "description"})['content']

        dict = {'title': title, 'description': description}
        print(dict)

    except Exception as e:
        print(e)
