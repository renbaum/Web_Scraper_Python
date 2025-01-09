import re
import shutil
import string
import os
import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
#    print("Input the URL:")
    pages = int(input())
    types = input()
    type_list = types.split(" ")
    base_url = "https://www.nature.com"
    main_url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"

    try:
        for i in range(1, pages + 1):
            url = f"{main_url}&page={i}"
            #if "nature.com" not in url: raise Exception("Invalid page!")
            response = requests.get(url)
            if(response.status_code != 200):
                raise Exception(f"The URL returned {response.status_code}!")

            # create the directory

            # Create directory for the current page
            dir_name = f"Page_{i}"
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
            os.makedirs(dir_name)

            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('article')
            for article in articles:
                article_type = article.find("span", {"data-test": "article.type"})
                tocontinue = False

                if article_type.text.strip() == types:
                    tocontinue = True

#                for types in type_list:
#                    if types == article_type.text.strip():
#                        tocontinue = True
#                        break
                if tocontinue:
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

                        with open(f"{dir_name}\\{f1}.txt", "wb") as f:
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
