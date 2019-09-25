import requests
from bs4 import BeautifulSoup
from IdPass import IdPass
from datetime import datetime


class WordMeaning:

    # initialization
    def __init__(self):

        # word to be searched.
        self.word = ''
        # defination of the word
        self.defination = ''

        
        self.searchUrl = 'https://www.dictionary.com/browse/{}?s=t'
        self.response = ''

    # assign word taken as input from the user.
    def readWord(self,word):
        self.word = word
    
    def search(self):
        # Using web search on dictonary.com to 
        # get the meaning.
        self.searchUrl = self.searchUrl.format(self.word)
        
        # response from the url
        self.response = requests.get(self.searchUrl)

        # beautifulSoup used to parse the html 
        # file i.e. to extract data from the 
        # html file
        soup = BeautifulSoup(self.response.text,'html.parser')

        # the defination of the word is defined 
        # in the meta tag of the url
        metaTags = soup.findAll('meta')
        
        # filtering
        # <meta name='description' 
        # content='Our required Defination'>
        for meta in metaTags:
            if meta.has_attr('name'):
                if meta.get('name')  == 'description':

                    # defination
                    self.defination = meta.get('content')
        print("Search Complete.")

    # formatting the defination
    def clean(self):
        # first occurence of , replace with ':'
        self.defination = self.defination.replace(',',':',1)
        # remove See more from the end.
        self.defination = self.defination.replace(' See more.','')
        # keeping each defination of the word
        # in different line
        self.defination = self.defination.replace(';','\n\t')
        # seperating the word from defination
        self.defination = self.defination.replace(' ','\n',1)
        # ToggleCasing
        self.defination = self.defination.replace('definition','Definition',1)

        self.defination = "Word Searched : " + self.defination
        print("Clean Complete.")

    # to create and maintain Log of the word searched
    # daily
    def createLog(self):
        # filename of the log file with date
        filename = 'Search_Logs_' + datetime.now().strftime("%d-%m-%Y") + '.txt'

        # opening the file in append mode
        fObj = open('Logs/' + filename,'a')

        # Time of creatim of the log file
        log = 'TimeStamp : ' + datetime.now().strftime("%H:%M:%S")

        # log containing the time word and defination
        log = log + "\n" + self.defination

        fObj.write(log)
        fObj.write('''\n------------------------------------------------------------------------------
------------------------------------------------------------------------------\n\n\n''')

        fObj.close()
        print('Create Log Complete.')
    
    # get Meaning of the word
    def getMeaning(self,word):
        # assign word
        WordMeaning.readWord(self,word)
        # search
        WordMeaning.search(self)
        # clean
        WordMeaning.clean(self)
        # createLog
        WordMeaning.createLog(self)
        # return
        return self.defination

if __name__ == '__main__':
    print("Hi")
    word = input('Enter the word to be searched')
    wMean = WordMeaning()
    print(wMean.getMeaning(word))