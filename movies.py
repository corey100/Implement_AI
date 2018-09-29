# Python3 code for movie
# recommendation based on
# emotion

# Import library for web
# scrapping
from bs4 import BeautifulSoup as SOUP
import re
import requests as HTTP
import urllib
import urllib2


# Main Function for scraping
def main(emotion):
    # IMDb Url for Drama genre of
    # movie against emotion Sad
    if (emotion == "Sad"):
        urlhere = 'http://www.imdb.com/search/title?genres=drama&title_type=feature&sort=moviemeter, asc'

    # IMDb Url for Musical genre of
    # movie against emotion Disgust
    elif (emotion == "Disgust"):
        urlhere = 'http://www.imdb.com/search/title?genres=musical&title_type=feature&sort=moviemeter, asc'

    # IMDb Url for Family genre of
    # movie against emotion Anger
    elif (emotion == "Anger"):
        urlhere = 'http://www.imdb.com/search/title?genres=family&title_type=feature&sort=moviemeter, asc'

    # IMDb Url for Thriller genre of
    # movie against emotion Anticipation
    elif (emotion == "Anticipation"):
        urlhere = 'http://www.imdb.com/search/title?genres=thriller&title_type=feature&sort=moviemeter, asc'

    # IMDb Url for Sport genre of
    # movie against emotion Fear
    elif (emotion == "Fear"):
        urlhere = 'http://www.imdb.com/search/title?genres=sport&title_type=feature&sort=moviemeter, asc'

    # IMDb Url for Thriller genre of
    # movie against emotion Enjoyment
    elif (emotion == "Enjoyment"):
        urlhere = 'http://www.imdb.com/search/title?genres=thriller&title_type=feature&sort=moviemeter, asc'

    # IMDb Url for Western genre of
    # movie against emotion Trust
    elif (emotion == "Trust"):
        urlhere = 'http://www.imdb.com/search/title?genres=western&title_type=feature&sort=moviemeter, asc'

    # IMDb Url for Film_noir genre of
    # movie against emotion Surprise
    elif (emotion == "Surprise"):
        urlhere = 'http://www.imdb.com/search/title?genres=film_noir&title_type=feature&sort=moviemeter, asc'

    # HTTP request to get the data of
    # the whole page
    response = HTTP.get(urlhere)
    data = response.text

    # Parsing the data using
    # BeautifulSoup
    soup = SOUP(data, "lxml")

    # Extract movie titles from the
    # data using regex
    title = soup.find_all("a", attrs={"href": re.compile(r'\/title\/tt+\d*\/')})
    return title


def getYoutubeLink(seacrhText):
    query = urllib.quote(seacrhText)
    url = "https://www.youtube.com/results?search_query=" + query
    # response = urllib2.urlopen(url)
    response = HTTP.get(url)
    # html = response.read()
    html = response.text
    soup = SOUP(html, "lxml")
    videos = soup.findAll(attrs={'class': 'yt-uix-tile-link'})

    # Print all video links from query
    # for vid in videos:
    #     print('https://www.youtube.com' + vid['href'])

    embeddedLink = None

    firstVideo = videos[0]
    if "watch" in firstVideo['href']:
        # print(firstVideo['href'])
        # print('https://www.youtube.com' + firstVideo['href'])
        # print(' ')

        # str = "<iframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed/jOGCNX8rBWs?rel=0&amp;showinfo=0\" frameborder=\"0\" allow=\"autoplay; encrypted-media\" allowfullscreen></iframe>"

        prefix = "<iframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed"
        key = firstVideo['href']
        suffix = "?rel=0&amp;showinfo=0\" frameborder=\"0\" allow=\"autoplay; encrypted-media\" allowfullscreen></iframe>"

        embeddedLink = prefix + key + suffix

    return embeddedLink

# Driver Function
if __name__ == '__main__':

    emotion = input("Enter the emotion: ")
    a = main(emotion)

    parsedTitles = []
    parsedLinks = []
    parsedDescriptions = []
    embeddedVideos = []

    count = 0
    for i in a:
        tmp = str(i).split('>')

        if (len(tmp) == 3):
            title = tmp[1][:-3]
            print(title)
            parsedTitles.append(title)
            parsedLinks.append("https://www.imdb.com" + tmp[0][9:-1])
            print(getYoutubeLink(title + "trailer"))

        if (count > 11):
            break
        count += 1
