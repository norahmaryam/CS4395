# Aleena Syed and Norah Khan
# CS 4395.001
# Web Crawler Assignment
from bs4 import BeautifulSoup
import requests
from bs4.element import Comment
from nltk.tokenize import sent_tokenize
from rake_nltk import Rake

# get links from starting url
def get_links(url):
    # get url
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')

    # add visited links to set
    visited_links = set()
    for link in soup.find_all('a'):
        link_str = str(link.get('href'))
        if link_str is not None and link_str.startswith('http') or link_str.startswith('https') and 'google' not in link_str:
            visited_links.add(link_str + '\n')
        if len(visited_links) > 15:
            break
    # write links to file
    write_to_file(visited_links)
    return visited_links

# write links to a file
def write_to_file(links):
    with open('data.txt', 'a') as f:
        f.writelines(links)

# return list of links
def get_all_links(url):
    visited_urls = set()
    visited_urls = get_links(url)
    return visited_urls

# returns visible elements in HTML
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# scrape text from webpage
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()    
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

# save text to files
def saveToFiles(links):
    url_index = 1
    i = 0
    list_of_files = []

    # create list of files
    for _ in range(len(links)):
        filename = "url" + str(url_index) + ".text"
        list_of_files.append(filename)
        url_index += 1

    # for each link, write to a file
    for link in links:
        html = requests.get(link)
        data = html.text
        text = text_from_html(data)
        with open(list_of_files[i], 'w') as f:
            f.write(text)
        i += 1
    return list_of_files

# process text
def processText(list_of_files):

    list_of_processed_files = []

    # write processed files to a file
    url_index = 1
    for file in list_of_files:
        with open(file, 'r') as f:
            lines = f.readlines()
            updated_filename = "updatedurl" + str(url_index) + ".text"
            # for each line in text, lowercase and strip white spaces
            for line in lines:
                line = line.strip()
                line = line.lower()
                sent_toks = sent_tokenize(line)
                updated_filename = "updatedurl" + str(url_index) + ".text"
                list_of_processed_files.append(updated_filename)
                with open(updated_filename, 'w') as h:
                    for sent in sent_toks:
                        h.write(sent)
                        h.write('\n')
            url_index += 1
    return list_of_processed_files

# extract important phrases using Rake API
def extractImportantTerms(list_of_processed_files):
    r = Rake()
    for file in list_of_processed_files:
        with open(file, 'r') as f:
            text = f.read()
            # return top 10 important phrases in each file
            r.extract_keywords_from_text(text)
            if 'philosophy' in r.get_ranked_phrases():
                print(r.get_ranked_phrases()[:25])
            print('\n')
    # manually return important terms
    important_terms = ['german', 'idealism', 'human', 'ideal', 'ideas', 'important', 'knowledge', 'metaphysics', 'philosophy', 'meaning']
    return important_terms
          
# starter url
r = 'https://en.wikipedia.org/wiki/Solipsism'
write_to_file([r])
# get visited links
visited_urls = get_all_links(r)
# write text of each webpage to each file
list_of_files = saveToFiles(visited_urls)
# process text
list_of_processed_files = processText(list_of_files)
# return important keywords
important_terms = extractImportantTerms(list_of_files)

