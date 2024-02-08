from markdownify import markdownify as md
from bs4 import BeautifulSoup
import glob

path = '/Users/brian/Documents/LaVida/team/ENGINEERIN'
all_files = glob.glob(f'{path}/**.html', recursive=True)

for html_file in all_files:
    with open(html_file, 'r', encoding="utf-8") as f:
        html_content = f.read()
        markdown = md(html_content)
        # print(markdown)

        soup = BeautifulSoup(html_content, 'html.parser')
        breadcrumbs = soup.find(id='breadcrumbs')
        if breadcrumbs is None:
            continue
        title = soup.find('title').text
        aaaa = breadcrumbs.text.replace('\n', '').replace('EngineeringEngineering', '').replace(
            'EngineeringEngineeringSprints-', '').strip()
        bbb = title.replace('Engineering : ', '')
        ccc = f'{aaaa}{bbb}'.replace('/', '')
        print(ccc)

        fo = open(f'{ccc}.md', "w", encoding="utf-8")
        fo.write(markdown)
        fo.close()