#!/usr/bin/env python

from mrjob.job import MRJob
from mrjob.step import MRStep
import json
import re

class TwitterMRJob(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.tweet_filter),
            MRStep(mapper=self.tweet_graph)
        ]
    
    def tweet_filter(self, _, line):
        tweetJson = json.loads(line)
        user = tweetJson['user']['name']
        #Removing non alphanumeric characters. Problem: user: I'm Jerry ;
        user = ''.join(c for c in user if c.isalnum())
        #Removing unicodes
        user = user.encode('ascii','ignore')
        user = user.decode("ascii")
        user = user.strip()
        tweet = tweetJson['text']
        #Removing control characters \n \r \t
        tweet = re.sub(r'[\n\r\t]', ' ', tweet)
        words = tweet.split (' ')
        hashtag = []
        for word in words:
            if "#" in word:
                #Removing unicodes
                word = word.encode('ascii','ignore')
                word = word.decode("ascii")
                word = word.strip()
                #Converting to lowercase
                word = word.lower()
                #Removing non alphanumeric characters
                word = ''.join(c for c in word if c.isalnum() or c =='#')
                hashtag.append(word)
        yield user, hashtag
        
    def tweet_graph(self, user, hashtag):
        # This import avoid the error described bellow when we use 
        # from py2neo import Graph and execute the script in hadoop-streaming  
        # Error: java.lang.RuntimeException: PipeMapRed.waitOutputThreads():
        #subprocess failed with code 1
        import sys
        sys.path.insert(0, '/srv/conda/envs/notebook/lib/python3.7/site-packages')

        from py2neo import Graph
        graph = Graph("bolt://127.0.0.1:7687")
        for index, aux in enumerate(hashtag):
            query1 = """MERGE (person:User{id: '"""+user+"""'}) MERGE (tw:Hashtag{hashtag:'"""+aux+"""'}) CREATE (person)-[:tweeted]->(tw)"""
            graph.run(query1)
            i=index
            while i < len(hashtag)-1:
                    query2 = """MERGE (tw1:Hashtag{hashtag: '"""+hashtag[index]+"""'}) MERGE (tw2:Hashtag{hashtag:'"""+hashtag[i+1]+"""'}) CREATE (tw1)-[:together]->(tw2)"""
                    graph.run(query2)
                    i+=1

if __name__ == '__main__':
    TwitterMRJob.run()
