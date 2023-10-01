import requests
from bs4 import BeautifulSoup

url = "https://www.wordunscrambler.net/word-list/wordle-word-list"

response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')

words = []
li_tags = soup.find_all('li', class_='invert light')
for li_tag in li_tags:
    a_tag = li_tag.find('a')
    if a_tag:
        words.append(a_tag.text.strip())

output_file = 'words.txt'
with open(output_file, 'w') as file:
    for word in words:
        file.write(word + '\n')

print('Words scraped and saved to', output_file)
