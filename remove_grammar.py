from bs4 import BeautifulSoup

file_path = 'Sanskrit_Project_Slides.html'

with open(file_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Find all list items containing the grammar section and remove them
for grammar_div in soup.find_all('div', class_='grammar-section'):
    # Find the parent li and remove it
    parent_li = grammar_div.find_parent('li')
    if parent_li:
        parent_li.decompose()

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("Successfully removed grammar sections.")
