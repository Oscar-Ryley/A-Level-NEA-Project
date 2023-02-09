from frequency_analysis import (
    create_frequency_list
    )
from requests import get
from bs4 import BeautifulSoup
from time import sleep

def get_text(URL: str):
    """Function: get_text
    @params
    URL: an input url for a given webpage

    Returns the paragraphs and header text of a website via web scraping.
    """
    try:
        page = get(URL)
        html = page.text
        soup = BeautifulSoup(html, "html.parser")
        page_text = soup.find_all("p")
        paragraphs = []
        for i in page_text:
            paragraphs.append(i)
        header = soup.find_all("h1")
    except:
        paragraphs = "No Internet"
        header = ""
    return paragraphs, header

def purge_tags(extract: list):
    """Function: purge_tags
    @params
    extract: the paragraphs of an extract of text, each paragraph is an item in the list

    Removes everything between the '<' and '>' characters and returns the resulting extract.
    """
    purging = list(str(extract))
    purged = []
    x = 0
    for l in range(0, len(purging)-1):
        letter = purging[l]
        if letter == "<":
            x = 1
        if x == 1 and letter !=">":
            pass
        elif letter == ">":
            x = 0
        else:
            purged.append(letter)

    final = "".join(purged)
    return final

def output_text(get_function, output_textfile: str):
    """Function: output_text
    @params
    get_function: a function which gets the text from a website via web scraping
    output_textfile: the name of the file to output 

    Returns the header of a get request, and outputs its body text into a given file.
    """
    text, header = get_function
    file = open(output_textfile, "w")
    for line in text:
        try:
            file.write(line)
        except:
            pass
    file.close
    return header

def output_any_text(text: str, output_textfile: str):
    """Function: output_text
    @params
    text: the text from a website that has been taken via web scraping
    output_textfile: the name of the file to output 

    Outputs the text parameter into a given file.
    """
    file = open(output_textfile, "w")
    for line in text:
        try:
            file.write(line)
        except:
            pass
    file.close

## BASIC
#Merriam-Webster - Basic Definition

def get_websterURL(query: str):
    """Function: get_websterURL
    @params
    query: the string query inputted by the user

    Returns a formulaic Merriam-Webster link from a given search query.
    """
    query = query.replace(" ", "%20")
    return "https://www.merriam-webster.com/dictionary/"+str(query)

def get_webster(query: str):
    """Function: get_webster
    @params
    query: the string query inputted by the user

    Returns the text and header from a Web Scrape of the Merriam-Webster article based on a given search query.
    """
    webster_paragraphs = []
    lines, header = get_text( get_websterURL( query ) )
    for line in lines:
        webster_paragraphs.append(purge_tags(line))
    header = purge_tags(header)
    header = header[1:]
    final = []
    x = -1
    for line in webster_paragraphs:
        x += 1
        if x < len(webster_paragraphs) -26:
            final.append(line)
    return str("\n".join(final)), header

def webster(query: str):
    """Function: webster
    @params
    query: the string query inputted by the user

    The main Merriam-Webster function, collates the other two.
    Interfaces with a file, merriam-webster_output.txt, in order to save the raw web scrape data.
    Returns the header, link and freq_list of a given webster article's web scrape.
    """
    header = output_text(get_webster(query), "C:/Users/Oscar/Documents/NEA/NEA/Webscrape_Output/merriam-webster_output.txt")
    freq_list = create_frequency_list("C:/Users/Oscar/Documents/NEA/NEA/Webscrape_Output/merriam-webster_output.txt")
    link = get_websterURL(query)
    return header, link, freq_list

#Britannica - Basic Meaning

def get_britannica_searchURL(query: str):
    """Function: get_britannicaURL
    @params
    query: the string query inputted by the user

    Returns a formulaic Britannica link from a given search query.
    """
    query = query.replace(" ", "+")
    return "https://www.britannica.com/search?query="+str(query)

def get_top_britannicaURL(query: str):
    try:
        page = get(get_britannica_searchURL(query))
        soup = BeautifulSoup(page.content, "html.parser")
        titles = soup.find_all(class_ = "mb-45 RESULT-1")
        link = str("https://www.britannica.com" + str(titles[0].find("a")["href"]))
        title = purge_tags(str(titles[0].find("a")))
        return link, title.split("\n\t\t\t\t\t")[1]
    except:
        return "https://www.britannica.com/", ""

def get_britannica(query: str):
    """Function: get_britannica
    @params
    query: the string query inputted by the user

    Web Scrapes from a Britannica article and outputs the paragraphs and header.
    """
    britannica_paragraphs = []
    link, header = get_top_britannicaURL(query)
    lines, _ = get_text( link )
    x = 0
    for line in lines:
        l = purge_tags(line)
        if x > 1 and l != "":
            britannica_paragraphs.append( l)
        else:
            x += 1
    return str("\n".join(britannica_paragraphs)), header, link

def britannica(query: str):
    """Function: britannica
    @params
    query: the string query inputted by the user

    The main britannica function, collates the other two functions.
    Returns the header, link and frequency list of a Britannica article given the search query.
    Also interfaces with a file in order to save the raw data from the web scrape.
    """
    paragraphs, header, link = get_britannica(query)
    output_any_text(paragraphs, "C:/Users/Oscar/Documents/NEA/NEA/Webscrape_Output/britannica_output.txt")
    freq_list = create_frequency_list("C:/Users/Oscar/Documents/NEA/NEA/Webscrape_Output/britannica_output.txt")
    return header, link, freq_list

#Dictionary.com - Basic Definition

def get_dictionaryURL(query: str):
    """Function: get_dictionaryURL
    @params
    query: the string query inputted by the user

    Returns a formulaic Dictionary.com link from a given search query.
    """
    query = query.replace(" ", "%20")
    return "https://www.dictionary.com/browse/" + query

def get_dictionary(query: str):
    """Function: get_dictionary
    @params
    query: the string query inputted by the user

    Webscrapes from a Dictionary.com search from a given search query.
    Returns the body paragraphs and header for this search (with first letter missing due to extra '[' character).
    """
    paragraphs, header = get_text(get_dictionaryURL(query))
    return purge_tags(paragraphs)[1:], purge_tags(header)[1:]

def dictionary(query: str):
    """Function: dictionary
    @params
    query: the string query inputted by the user

    The main dictionary function, which collates the other two functions.
    Returns the header, link and freq_list from a Dictionary.com search web scrape given a query.
    Also interfaces with a file in order to save the raw data from the web scrape.
    """
    header = output_text(get_dictionary(query), "C:/Users/Oscar/Documents/NEA/NEA/Webscrape_Output/dictionary_output.txt")
    freq_list = create_frequency_list("C:/Users/Oscar/Documents/NEA/NEA/Webscrape_Output/dictionary_output.txt")
    link = get_dictionaryURL(query)
    return header, link, freq_list

#BBC Bitesize - Basic Articles

def get_bitesize_searchURL(query: str):
    """Function: get_bitesize_searchURL
    @params
    query: the string query inputted by the user

    Returns a formulaic BBC Bitesize search result URL based on a given search query.
    """
    query = query.replace(" ", "+")
    return "https://www.bbc.co.uk/bitesize/search?q=" + query + "&d=BITESIZE"

def get_bitesize_articleURL(query: str):
    """Function: get_bitesize_articleURL
    @params
    query: the string query inputted by the user

    Returns the first article link and title from a BBC bitesize search.
    """
    try:
        page = get(get_bitesize_searchURL(query))
        soup = BeautifulSoup(page.content, "html.parser")
        titles = soup.find_all(class_ = "ssrcss-1f3bvyz-Stack e1y4nx260")
        return str(titles[0].find("a")["href"]), str(titles[0].find("p"))
    except:
        return "https://www.bbc.co.uk/bitesize/", ""

def get_bitesize(query: str):
    """Function: get_bitesize
    @params
    query: the string query inputted by the user

    Web scrapes from a specific BBC Bitesize article and returns the paragraphs, title and link from the article given the search query.
    """
    link, title = get_bitesize_articleURL(query)
    paragraphs, _ = get_text(link)
    paragraphs = purge_tags(paragraphs)[2:]
    return paragraphs, title, link

def bitesize(query: str):
    """Function: get_bitesize_articleURL
    @params
    query: the string query inputted by the user

    The main bitesize function, which collates the other three functions.
    Returns the title, link and freqlist from the bitesize article given a search query.
    Also interfaces with a file in order to save the raw data from the web scrape.
    """
    paragraphs, header, link = get_bitesize(query)
    output_any_text(paragraphs, "C:/Users/Oscar/Documents/NEA/NEA/Webscrape_Output/bitesize_output.txt")
    freqlist = create_frequency_list("C:/Users/Oscar/Documents/NEA/NEA/Webscrape_Output/bitesize_output.txt")
    title = purge_tags(header)
    return title, link, freqlist

## INTERMEDIATE
#Wikipedia - Intermediate Source

def remove_wikicites(extract: list):
    """Function: remove_wikicites
    @params
    extract: the text extract (list with each item as each paragraph)

    Returns a version of the list without any of the text between the '[' and ']' characters.
    Does not save any numbers in between these characters specifically.
    """
    removing = list(str(extract))
    removed = []
    x = 0
    for l in range(0, len(removing)-1):
        letter = removing[l]
        if letter == "[":
            x = 1
        if x == 1 and letter !="]" or x==1 and letter.isnumeric() == True:
            pass
        elif letter == "]":
            x = 0
        else:
            removed.append(letter)
    final = "".join(removed)
    return final 

def get_wikiURL(query: str):
    """Function: get_wikiURL
    @params
    query: the string query inputted by the user

    Returns a formulaic wikipedia article from a given search query. 
    """
    query = query.title()
    query = query.replace(" ", "_")
    return "https://en.wikipedia.org/wiki/"+str(query)

def get_wikipedia(query: str):
    """Function: get_wikipedia
    @params
    query: the string query inputted by the user

    Web scrapes from a given wikipedia article given a search query.
    Returns the paragraphs  from the article, as well as the title of the article.
    """
    wiki_paragraphs = []
    paragraphs, header = get_text( get_wikiURL( query ) )
    for para in paragraphs:
        p = remove_wikicites(purge_tags(para))
        if p != "":
            wiki_paragraphs.append( p )
    header = purge_tags(header)
    header = header[1:]
    return str("\n".join(wiki_paragraphs[1:])), header

def wikipedia(query: str):
    """Function: wikipedia
    @params
    query: the string query inputted by the user

    The main wikipedia function, collates the other three functions.
    Returns the title, link and freq_list from a given wikipedia article based on the parameter search query.
    Also interfaces with a file in order to save the raw data from the web scrape.
    """
    header = output_text(get_wikipedia(query), "C:/Users/Oscar/Documents/NEA/NEA/Webscrape_Output/wikipedia_output.txt")
    freq_list = create_frequency_list("C:/Users/Oscar/Documents/NEA/NEA/Webscrape_Output/wikipedia_output.txt")
    title = header
    link = get_wikiURL(query)
    return title, link, freq_list

#SparkNotes - Intermediate Source

def get_sparkURL(query: str):
    """Function: get_sparkURL
    @params
    query: the string query inputted by the user

    Returns a formulaic SparkNotes search URL from a given search query. 
    """
    return "https://www.sparknotes.com/search?q=" + query

def get_top_sparkURL(query: str):
    """Function: get_top_sparkURL
    @params
    query: the string query inputted by the user

    Web scrapes from a SparkNotes search URL in order to return the name and link of the top search result.
    """
    try:
        page = get(get_sparkURL(query))
        soup = BeautifulSoup(page.content, "html.parser")
        article_titles = soup.find_all(class_ = "search-result-block top-result lit-search-icon")
        name = article_titles[0].find("h3")
        name = purge_tags(name)
        link = "https://www.sparknotes.com/" + str(article_titles[0].find("a")["href"])
    except:
        name = ""
        link = "https://www.sparknotes.com/"
    return name, link

def sparknotes(query: str):
    """Function: sparknotes
    @params
    query: the string query inputted by the user

    Web scrapes from the SparkNotes article.
    Then removes all of the unnecessary text information from the web scrape.
    And outputs the raw text to the file, as well as returning the header, link and freq_list of the source.
    """
    name, link = get_top_sparkURL(query)
    text = purge_tags(get_text(link))
    try:
        sparkextract = text.split("Please wait while we process your payment, Your PLUS subscription has expired, Please wait while we process your payment, ")[1]
    except:
        sparkextract = ""
    output_any_text(sparkextract, "C:/Users/Oscar/Documents/NEA/NEA/Webscrape_Output/sparknotes_output.txt")
    freq_list = create_frequency_list("C:/Users/Oscar/Documents/NEA/NEA/Webscrape_Output/sparknotes_output.txt")
    header = name.strip()
    return header, link, freq_list

#BookSummary - Intermediate Source

def get_booksummary_searchURL(query: str):
    """Function: get_booksummary_searchURL
    @params
    query: the string query inputted by the user

    Returns a formulaic BookSummary.net search URL based on a given search query.
    """
    query = query.replace(" ", "+")
    return "https://www.booksummary.net/?s=" + query

def get_booksummary_articleURL(query: str):
    """Function: get_booksummary_articleURL
    @params
    query: the string query inputted by the user

    Returns the first article link and title from a booksummary.net search.
    """
    try:
        page = get(get_booksummary_searchURL(query))
        soup = BeautifulSoup(page.content, "html.parser")
        title = soup.find(class_ = "entry-title")
        link = title.find("a")["href"]
        text = title.find(class_ = "entry-title-link") 
        return link, purge_tags(text)
    except:
        return "https://www.booksummary.net/", ""

def get_booksummary(query: str):
    """Function: get_booksummary
    @params
    query: the string query inputted by the user

    Web scrapes from a specific booksummary article and returns the paragraphs, title and link from the article given the search query.
    """
    link, title = get_booksummary_articleURL(query)
    paragraphs, _ = get_text(link)
    paragraphs = purge_tags(paragraphs)
    try:
        paragraphs = paragraphs.split(", Book Summary, booksummary.net,")[1]
        paragraphs = paragraphs.split("Your email address will not be published")[0]
    except:
        pass
    return paragraphs, title, link

def booksummary(query: str):
    """Function: wikipedia
    @params
    query: the string query inputted by the user

    The main booksummary function, collates the other three functions.
    Returns the title, link and freq_list from a given booksummary.net article based on the parameter search query.
    Also interfaces with a file in order to save the raw data from the web scrape.
    """
    paragraphs, title, link = get_booksummary(query)
    output_any_text(paragraphs, "C:/Users/Oscar/Documents/NEA/NEA/Webscrape_Output/booksummary_output.txt")
    freqlist = create_frequency_list("C:/Users/Oscar/Documents/NEA/NEA/Webscrape_Output/booksummary_output.txt")
    return title, link, freqlist

#History.com - Intermediate Source

def get_history_searchURL(query: str):
    """Function: get_history_searchURL
    @params
    query: the string query inputted by the user

    Returns a formulaic history.com URL based on a given search query.
    """
    query = query.replace(" ", "%20")
    return "https://www.history.co.uk/search/node?keys=" + query

def get_history_articleURL(query: str):
    """Function: get_history_articlehURL
    @params
    query: the string query inputted by the user

    Returns the link and title of the first article from a history.com search.
    """
    try:
        page = get(get_history_searchURL(query))
        soup = BeautifulSoup(page.content, "html.parser")
        first = soup.find(class_ = "list-group-item col-card")
        link = first.find("a")["href"]
        title = first.find("h5")
        return link, purge_tags(title)
    except:
        return "https://www.history.co.uk/", ""

def get_history(query: str):
    """Function: get_history
    @params
    query: the string query inputted by the user

    Returns the paragraphs, title and link that are web scraped from a history.com search.
    """
    link, title = get_history_articleURL(query)
    paragraphs, _ = get_text(link)
    paragraphs = purge_tags(paragraphs)[1:]
    return paragraphs, title, link

def history(query: str):
    """Function: history
    @params
    query: the string query inputted by the user

    Final history.com search function, uses the other three functions.
    Returns the title, link and freqlist for a history.com article given a search query.
    """
    paragraphs, title, link = get_history(query)
    output_any_text(paragraphs, "C:/Users/Oscar/Documents/NEA/NEA/Webscrape_Output/history_output.txt")
    freqlist = create_frequency_list("C:/Users/Oscar/Documents/NEA/NEA/Webscrape_Output/history_output.txt")
    return title, link, freqlist

## ARTICLES
#Reuters - Journalistic Articles

def get_reuters_searchURL(query: str):
    """Function: get_retuers_searchURL
    @params
    query: the string query inputted by the user

    Returns a formulaic Reuters search URL from a given search query.
    Replaces all spaces in the search query with '%20' in order to make it more legible to the search.
    """
    query = query.replace(" ", "%20")
    return "https://www.reuters.com/search/news?sortBy=&dateRange=&blob=" + query

def get_reuters_articleURL(query: str):
    """Function: get_retuers_articleURL
    @params
    query: the string query inputted by the user

    Web Scrapes from a Reuters search URL in order to return the names and links of the top search results.
    Exception handling for no internet or unable to make search returns blank names and links.
    """
    try:
        page = get(get_reuters_searchURL(query))
        soup = BeautifulSoup(page.content, "html.parser")
        links = []
        article_titles = soup.find_all(class_= "search-result-title")
        for article in article_titles:
            try:
                links.append("https://www.reuters.com" + str(article.find("a")["href"]))
            except:
                article_titles.remove(article)
        titles = []
        for title in article_titles:
            titles.append(title.text)
        output_list = []
        for index in range(0, len(titles)):
            try:
                output_list.append([titles[int(index)], links[int(index)]])
            except:
                break
        for item in output_list:
            if item[0].find("REFILE") != -1 or item[0].find("UPDATE"):
                output_list.remove(item)
    except:
        output_list = []
        for i in range(0, 4):
            output_list.append( [str(i), "https://www.reuters.com"] )
    return output_list

def get_reuters(article_title: str, articleURL: str):
    """Function: get_retuers
    @params
    article_title: Title of the article
    articleURL: URL of the article to be Web Scraped

    Returns the Header, URL and body text Web Scraped from a specific Reuters article.
    """
    html, header = get_text( articleURL )
    header = article_title
    body_text, separator, another_article = (purge_tags(html)).partition("Our Standards: The Thomson Reuters Trust Principles")
    return header, articleURL, body_text

def reuters(query: str):
    """Function: reuters
    @params
    query: the string query inputted by the user

    Returns the Header, URL and body text from the top four reuters URLs given an inputted query.
    As error catching for no internet, a blank reuters_output is created and returned.
    Also interfaces with a file in order to save the raw data from the web scrape.
    """
    articles = get_reuters_articleURL(query)
    reuters_output = []
    index = 0
    while len(reuters_output) != 4:
        try:
            x = 1
            file = "C:/Users/Oscar/Documents/NEA/NEA/Webscrape_Output/reuters" + str(index+1) + "_output.txt"
            header, link, paragraphs = get_reuters(articles[index][0], articles[index][1])
            output_any_text(paragraphs, file)
            freq_list = create_frequency_list(file)
            for i in reuters_output:
                if header == i[0]:
                    x = 0
            if x == 1:
                reuters_output.append([header, link, freq_list])
            index += 1
        except:
            reuters_output.append([str(index), "https://www.reuters.com", ["No Summary Available"]])
            index += 1
    if reuters_output == [['0', 'https://www.reuters.com', ['No Summary Available']], ['1', 'https://www.reuters.com', ['No Summary Available']], ['2', 'https://www.reuters.com', ['No Summary Available']], ['3', 'https://www.reuters.com', ['No Summary Available']]]:
        for i in reuters_output:
            i[0] = ""
    return reuters_output

## ACADEMIC   
#Google Scholar / Further Reading - Academic Sources

def remove_title_tags(title: str):
    """Function: remove_title_tags
    @params
    title: title of a google scholar article

    Returns the title parameter without any text between square brackets ('[' and ']').
    """   
    purging = list(str(title))
    purged = []
    x = 0
    for l in range(0, len(purging)):
        letter = purging[l]
        if letter == "[":
            x = 1
        if x == 1 and letter !="]":
            pass
        elif letter == "]":
            x = 0
        else:
            purged.append(letter)
    final = "".join(purged)
    return final

def get_scholar_searchURL(page_num: int, query: str):
    """Function: get_scholar_searchURL
    @params
    page_num: page number of the search
    query: search query for the search

    Returns a formulaic google scholar search URL based on the query and page number from the results you want to look at.
    Each page of the search results is identified by the tenth search of each result.
    """
    article_num = (page_num-1) *10
    page_value = "start=" + str(article_num) + "&"
    query = query.replace(" ", "+")
    return "https://scholar.google.com/scholar?" + page_value + "q=" + query

def get_scholar_articleURLs(scholarURL: str):
    """Function: get_scholar_articleURLs
    @params
    scholarURL: URL for a google scholar search

    Returns an output 2D array of google scholar article names and links to those articles.
    Uses the scholar search URL to scrape from.
    """
    try:
        sleep(0.5)
        page = get(scholarURL)
        soup = BeautifulSoup(page.content, "html.parser")
        links = []
        article_titles = soup.find_all("h3", class_= "gs_rt")
        titles = []
        for article in article_titles:
            try:
                if "CITATION" in article.text:
                    article_titles.remove(article)
                else:
                    links.append(article.find("a")["href"])
                    titles.append(article.text)
            except:
                article_titles.remove(article)
        output_list = []
        for i in range(0, len(titles)):
            try:
                output_list.append([titles[int(i)], links[int(i)]])
            except:
                break
    except:
        output_list = []
        for i in range(0, 8):
            if i % 2 == 0:
                output_list.append( ["", "https://scholar.google.com"] )
            else:
                output_list.append( ["[BOOK]", "https://scholar.google.com"] )
    return output_list

def get_scrapable(scholar_results: list):
    """Function: get_scrapable
    @params
    scholar_results: a list of names and links of google scholar search results

    Returns all of the results which are not books or pdfs (as these cannot have their text scraped from).
    """
    further_reading = []
    scrapable = []
    for i in scholar_results:
        if "[BOOK]" in  i[0] or "[PDF]" in i[0]:
            further_reading.append(i)
        else:
            scrapable.append(i)
    return scrapable, further_reading

def get_final_scholar_URLs(query: str):
    """Function: get_final_scholar_URLs
    @params
    query: the string query inputted by the user

    Returns a final list of google scholar search results, making sure to aim for 4 scholar and 4 further reading.
    If a page returns no results a few times, blank entries are returned.
    Checks multiple pages until the desired output is returned.
    """
    further_reading = []
    scrapable = []
    page = 1
    none_found = 0
    while len(scrapable) != 4 or len(further_reading) != 4:
        lengths = int(len(scrapable) + len(further_reading))
        more_scrapable, more_further_reading = get_scrapable(get_scholar_articleURLs(get_scholar_searchURL(page, query)))
        for i in more_scrapable:
            if len(scrapable) < 4:
                scrapable.append(i)
        for i in more_further_reading:
            if len(further_reading) < 4:
                further_reading.append(i)
        if len(scrapable) + len(further_reading) == lengths:
            if none_found == 2:
                while len(scrapable) != 4:
                    scrapable.append(["", "https://scholar.google.com/"])
                while len(further_reading) != 4:
                    further_reading.append(["", "https://scholar.google.com/"])
                break
            none_found += 1
        page += 1
    return scrapable, further_reading

def get_scholar(article_name: str, link: str):
    """Function: get_scholar
    @params
    article_name: the name of the article being scraped from
    link: link to the article being scraped from

    Webscrapes from a specific google scholar article and returns its body text, article name and link.
    """
    scholar_paragraphs = []
    sleep(0.5)
    lines, header = get_text( link )
    x = 0
    for line in lines:
        l = purge_tags(line)
        if x > 1 and l != "":
            scholar_paragraphs.append( l)
        else:
            x += 1
    header = remove_title_tags(str(article_name))
    return str("\n".join(scholar_paragraphs)), header, link

def scholar(query: str):
    """Function: scholar
    @params
    query: the string query inputted by the user

    Utilises the other scholar functions in order to web scrape from a google scholar search given a query.
    Finds the top 4 text articles and the top 4 books/ pdfs and returns them as scholar output and further reading list respectively.
    Also interfaces with a file in order to save the raw data from the web scrape of the scholar articles specifically.
    """
    scrapable, further_reading = get_final_scholar_URLs(query)
    scholar_output = []
    num = 1
    for i in scrapable:
        file = "C:/Users/Oscar/Documents/NEA/NEA/Webscrape_Output/scholar" + str(num) + "_output.txt"
        paragraphs, header, link = get_scholar(i[0], i[1])
        output_any_text(paragraphs, file)
        freq_list = create_frequency_list(file)
        scholar_output.append([header, link, freq_list])
        num += 1
    for i in further_reading:
        i[0] = remove_title_tags(i[0])
    return scholar_output, further_reading