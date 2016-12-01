'''
https://en.wiktionary.org/wiki/mononym
https://en.wikipedia.org/wiki/Khangar_(community)
https://en.wikipedia.org/wiki/Niraj_Sah
https://en.wikipedia.org/wiki/Ridge_Meadows_Frizz
https://en.wikipedia.org/wiki/Mero%C3%AB
https://en.wikipedia.org/wiki/Louis_William_Larsen
'''

import requests, re, sys
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup
from time import time
import matplotlib.pyplot as plt
import numpy as np


'''
Defining main body as paragraph text mentioned after first heading. Only <p> tags
https://en.wikipedia.org/wiki/Jonathan_Wells_(American_football)

Main body is defined as following:

Jonathan Wells (born July 21, 1979) is a former American football running back. He played
college football at Ohio State University and professionally in the National Football League
(NFL) with the Houston Texans.
'''

class HopToPhilosophyHash(object):
    def __init__(self):
        self.parent = {}
        self.parent['Philosophy'] = None
        self.deadends = set()
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
            return 1
        soup = BeautifulSoup(r.text,"lxml")

        localPath = []


        if firstTopic in self.parent:
            return self.calculateHopsDistance(firstTopic,localPath)
        if firstTopic in self.deadends:
            return None

        topic = firstTopic
        localPath.append(topic)

        redLink = 'redLink'
        wikiLink = 'wikiLink'
        isLoop = 'isLoop'
        noLink = 'noLink'

        while soup.find(id='firstHeading').text != 'Philosophy':
            pageStatus = {redLink: False, wikiLink: False, isLoop: False, noLink: False}
            content = soup.find(id='mw-content-text')

            # removing content box (toc), vertical box and navbox
            for t in content.find_all(class_=['navbox', 'vertical-navbox', 'toc']):
                t.replace_with("")

            # remove spans and smalls with language, pronounciation
            for s in content.find_all(['div', 'table']):
                s.replace_with("")

            # Keep looping through <p> elements
            paragraph = content.find("p")
            noLinkParas = 0
            countParagraphs = self.countParas(paragraph)

            if countParagraphs == 0:
                pageStatus[noLink] = True
                for each in localPath:
                    self.deadends.add(each)
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

                    value, flag = self.checkTopic(topic, localPath)
                    if flag:
                        return value

                    localPath.append(topic)
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
                    for each in localPath:
                        self.deadends.add(each)
                    return None

                elif firstLinkWithRed != None and firstLinkWithWiki != None:
                    text = str(reParagraph)
                    redLinkText = str(firstLinkWithRed)
                    wikiLinkText = str(firstLinkWithWiki)
                    wikiLinkIndex = text.find(wikiLinkText)
                    redLinkIndex = text.find(redLinkText)
                    if redLinkIndex < wikiLinkIndex:
                        pageStatus[redLink] = True
                        for each in localPath:
                            self.deadends.add(each)
                        return None
                    else:
                        topic = firstLinkWithWiki.get('href').split('/')[-1]
                        # print topic

                        value,flag = self.checkTopic(topic,localPath)
                        if flag:
                            return value

                        localPath.append(topic)
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
                for each in localPath:
                    self.deadends.add(each)
                return None

        for i in range(len(localPath)-1):
            self.parent[localPath[i]] = localPath[i+1]
        return len(localPath) - 1

    def calculateHopsDistance(self,topic,localPath):
        restofPath = []
        while topic != None:
            restofPath += [topic]
            topic = self.parent[topic]
        totalPath = localPath + restofPath
        for i,each in enumerate(totalPath):
            if each in self.parent:
                break
            self.parent[totalPath[i]] = totalPath[i + 1]
        return len(totalPath) - 1

    def countParas(self,p):
        countParagraphs = 0
        node = p
        while node:
            if node.name == 'p':
                countParagraphs += 1
                node = node.find_next_sibling()
            else:
                break
        return countParagraphs

    def checkTopic(self,topic,localPath):
        if topic in localPath:
            for each in localPath:
                self.deadends.add(each)
            return None,True
        if topic in self.deadends:
            for each in localPath:
                self.deadends.add(each)
            return None,True
        if topic in self.parent:
            return self.calculateHopsDistance(topic, localPath),True
        return None,False

if __name__ == "__main__":
    begin = time()
    h = HopToPhilosophyHash()
    s = 0
    cp = 0
    pathlengths = []
    timeTaken = []

    inp = sys.argv
    randomPages = int(inp[1])
    for i in range(randomPages):
        start = time()
        hops = h.getHops()
        if hops != None:
            s += hops
            cp += 1
            pathlengths.append(hops)
            timeTaken.append(time()- start)
        print

        print 'Random pages left: ', randomPages - i - 1
        print
    totalTime = time() - begin
    print
    if randomPages > 0:
        print 'Number of pages that landed to philosophy :', cp
        print 'Percentage pages landing to philosophy :', float(cp)/randomPages*100, '%'
        if cp != 0:
            print 'Average hops :', float(s)/cp
        else:
            print 'Average hops :', 0

        # Statistics
        l = len(pathlengths)
        pathlengths.sort()
        if l != 0 and l % 2 == 0:
            print 'Median of', l, ' random pages (that landed to philosophy) path lengths (number of hops) is', float(pathlengths[(l / 2) - 1] + pathlengths[(l / 2)]) / 2
        elif l != 0 and l % 2 != 0:
            print 'Median of', l, ' random pages (that landed to philosophy) path lengths (number of hops) is', float(pathlengths[(l / 2)])
        else:
            print 'Median of', randomPages, 'path lengths (number of hops) is', 0, '(No page landed to philosophy). '
        print 'Total time taken for',randomPages, 'random pages :', totalTime,'seconds','\n'
        print 'Total number of http requests made for all random pages :', h.httpreqs
        if randomPages == 500:
            x = np.asarray(pathlengths)
            plt.hist(x, normed=True, bins=30)
            plt.ylabel('No. of hops')
            plt.show()
            # plt.savefig('path-lengths-with-hashing.png')
    else:
        print 'No. of random pages is', randomPages
