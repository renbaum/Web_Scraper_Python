import re
import string

import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
#    print("Input the URL:")
#    url = input()
    base_url = "https://www.nature.com"
    url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3"

    try:
        #if "nature.com" not in url: raise Exception("Invalid page!")
        response = requests.get(url)
        if(response.status_code != 200):
            raise Exception(f"The URL returned {response.status_code}!")

        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')
        for article in articles:
            article_type = article.find("span", {"data-test": "article.type"})
            if article_type and article_type.text.strip() == "News":
                article_link_tag = article.find("a", {"data-track-action": "view article"})
                if article_link_tag and article_link_tag.get("href"):
                    article_url = base_url + article_link_tag["href"]

                    # Fetch the full article page
                    article_response = requests.get(article_url)
                    if article_response.status_code != 200:
                        print(f"Failed to fetch article: {article_url}. Skipping...")
                        continue

                    # Parse the full article HTML
                    article_soup = BeautifulSoup(article_response.content, "html.parser")
                    # Extract the title of the article
                    title_tag = article_soup.find("p", {"class": "article__teaser"})
                    if not title_tag:
                        print(f"Failed to extract title for article: {article_url}. Skipping...")
                        continue
                    body = title_tag.text.strip()

#                    filename = article_link_tag.text.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_') + ".txt"
                    punc = string.punctuation
                    punc = punc.replace("_", "")
                    punc += '’'
                    f1 = article_link_tag.text
                    f1 = f1.translate(str.maketrans(' ', '_'))
                    f1 = f1.translate(str.maketrans('', '', punc))

                    with open(f1 + ".txt", "wb") as f:
                        f.write(body.encode('utf-8'))
        # headers = {'Accept': 'application/json'}
        # response = requests.get(url).content

        #page_content = requests.get(url).content

#        with open("source.html", "wb")  as file:
#            file.write(response.content)

       # print("Content saved.")

#        titel = soup.find('title')
#        title = titel.text
#        description = soup.find('meta', attrs={"name": "description"})['content']

#        dict = {'title': title, 'description': description}
#        print(dict)

    except Exception as e:
        print(e)
