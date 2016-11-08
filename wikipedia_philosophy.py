'''
https://en.wiktionary.org/wiki/mononym
https://en.wikipedia.org/wiki/Khangar_(community)
https://en.wikipedia.org/wiki/Niraj_Sah
https://en.wikipedia.org/wiki/Ridge_Meadows_Frizz
https://en.wikipedia.org/wiki/Mero%C3%AB
'''
import requests, re , sys
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup
from time import time


'''
Defining main body as paragraph text mentioned after first heading. Only <p> tags
https://en.wikipedia.org/wiki/Jonathan_Wells_(American_football)

Main body is defined as following:

Jonathan Wells (born July 21, 1979) is a former American football running back. He played
college football at Ohio State University and professionally in the National Football League
(NFL) with the Houston Texans.
'''

class HopToPhilosophySimple(object):
    def __init__(self):
        self.parent = {}
        self.deadends = set()
        self.distanceFromPhilosophy = {}
        self.httpreqs = 0

    def getHops(self,url="https://en.wikipedia.org/wiki/Special:Random"):
        countHops = 0 # number of hops
        r = requests.get(url)
        self.httpreqs += 1
        # print r.status_code
        print r.url
        firstTopic = r.url.split('/')[-1]
        # print firstTopic
        if firstTopic == 'Philosophy':
            return countHops
        soup = BeautifulSoup(r.text,"lxml")
        flag = True
        path = []
        path.append(firstTopic)

        redLink = 'redLink'
        wikiLink = 'wikiLink'
        isLoop = 'isLoop'
        noLink = 'noLink'

        while soup.find(id='firstHeading').text != 'Philosophy':
            pageStatus = {redLink: False, wikiLink: False, isLoop: False, noLink: False}
            flag = False


            content = soup.find(id='mw-content-text')

            # removing content box (toc), vertical box and navbox
            for t in content.find_all(class_=['navbox', 'vertical-navbox', 'toc']):
                t.replace_with("")
            for s in content.find_all(['div', 'table']):  # remove spans and smalls with language, pronounciation
                s.replace_with("")

            # Keep looping through <p> elements
            paragraph = content.find("p")
            if paragraph == None:
                pageStatus[2] = True
                break

            countParagraphs = 0
            noLinkParas = 0

            node = paragraph
            while node:
                if node.name == 'p':
                    countParagraphs += 1
                    node = node.find_next_sibling()
                else:
                    break

            if countParagraphs == 0:
                pageStatus[noLink] = True
                return None

            for i in range(countParagraphs):

                if i == 0:
                    paragraph = content.find("p")
                else:
                    paragraph = paragraph.find_next_sibling()

                # clean paragraph
                for s in paragraph.find_all(['span', 'small', 'sup,', 'i', 'table']):
                    s.replace_with("")

                paragraphText = str(paragraph)

                # Remove leftover parenthesized text
                paragraphText = re.sub(r' \(.*?\)', '', paragraphText)

                # Souping it back into bs4 object to find links
                reParagraph = BeautifulSoup(paragraphText, "lxml")

                firstLinkWithRed = reParagraph.find(href=re.compile('^/w/'))
                firstLinkWithWiki = reParagraph.find(href=re.compile('^/wiki/'))

                if firstLinkWithRed == None and firstLinkWithWiki == None:
                    noLinkParas += 1
                    continue
                elif firstLinkWithRed == None and firstLinkWithWiki != None:
                    topic = firstLinkWithWiki.get('href').split('/')[-1]
                    # print topic
                    if topic in path:
                        return None
                    path.append(topic)
                    url = 'http://en.wikipedia.org' + firstLinkWithWiki.get('href')
                    print(url)
                    r = requests.get(url)  # Make new request
                    self.httpreqs += 1
                    soup = BeautifulSoup(r.text,"lxml")
                    countHops += 1
                    pageStatus[wikiLink] = True
                    break
                elif firstLinkWithRed != None and firstLinkWithWiki == None:
                    pageStatus[redLink] = True
                    return None
                elif firstLinkWithRed != None and firstLinkWithWiki != None:
                    text = str(reParagraph)
                    redLinkText = str(firstLinkWithRed)
                    wikiLinkText = str(firstLinkWithWiki)
                    wikiLinkIndex = text.find(wikiLinkText)
                    redLinkIndex = text.find(redLinkText)
                    if redLinkIndex < wikiLinkIndex:
                        pageStatus[redLink] = True
                        return None
                    else:
                        topic = firstLinkWithWiki.get('href').split('/')[-1]
                        # print topic
                        if topic in path:
                            return None
                        path.append(topic)
                        url = 'http://en.wikipedia.org' + firstLinkWithWiki.get('href')
                        print(url)
                        r = requests.get(url)  # Make new request
                        self.httpreqs += 1
                        soup = BeautifulSoup(r.text,"lxml")
                        countHops += 1
                        pageStatus[wikiLink] = True
                        break

            if noLinkParas == countParagraphs:
                pageStatus[noLink] = True
                return None

        return countHops

if __name__ == "__main__":

    h = HopToPhilosophySimple()
    begin = time()
    pathlengths = []
    timeTaken = []
    s = 0
    cp = 0
    inp = sys.argv
    randomPages = int(inp[1])

    for i in range(randomPages):
        start = time()
        hops = h.getHops()
        if hops != None:
            s += hops
            cp += 1
            pathlengths.append(hops)
            timeTaken.append(time() - start)
        print
        print 'Random pages left: ', randomPages - i - 1
        print

    totalTime = time() - begin
    print
    if randomPages > 0:
        print 'Number of pages that landed to philosophy :', cp
        print 'Percentage pages landing to philosophy :', float(cp)/randomPages*100, '%'
        if cp != 0:
            print 'Average hops for pages that landed to philosophy:', float(s) / cp
        else:
            print 'Average hops :', 0 , '(No page landed to philosophy). '

        #Statistics
        l = len(pathlengths)
        pathlengths.sort()
        if l !=0 and l%2 == 0:
            print 'Median of',l, ' random pages (that landed to philosophy) path lengths (number of hops) is', float(pathlengths[(l/2)-1]+pathlengths[(l/2)])/2
        elif l != 0 and l%2 != 0:
            print 'Median hops for pages that landed to philosophy: ', float(pathlengths[(l/2)])
        else:
            print 'Median hops for pages that landed to philosophy: is', 0 , '(No page landed to philosophy). '
        print 'Total time taken for', randomPages, 'random pages :', totalTime,'seconds','\n'
        print 'Total number of http requests made for all random pages :', h.httpreqs
    else:
        print 'No. of random pages is', randomPages