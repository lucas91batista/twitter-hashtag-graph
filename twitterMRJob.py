from mrjob.job import MRJob
from mrjob.step import MRStep
from py2neo import Graph
import json

class TwitterMRJob(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.tweet_filter),
            MRStep(mapper=self.tweet_graph)
        ]
    
    def tweet_filter(self, _, line):
        tweetJson = json.loads(line)
        user = tweetJson['user']['name']  
        tweet = tweetJson['text']
        words = tweet.split (' ')
        hashtag = []
        for word in words:
            if "#" in word:
                hashtag.append(word)
        yield user, hashtag
        
    def tweet_graph(self, user, hashtag):
        graph = Graph("bolt://127.0.0.1:7687")
        for index, aux in enumerate(hashtag):
            query1 = """MERGE (person:User{id: '"""+user+"""'}) MERGE (tw:Hashtag{hashtag:'"""+aux+"""'}) CREATE (person)-[:tweeted]->(tw)"""
            graph.run(query1)
            #consult=[]
            i=index
            while i < len(hashtag)-1:
                    query2 = """MERGE (tw1:Hashtag{hashtag: '"""+hashtag[index]+"""'}) MERGE (tw2:Hashtag{hashtag:'"""+hashtag[i+1]+"""'}) CREATE (tw1)-[:together]->(tw2)"""
                    #consult.append(query2)
                    graph.run(query2)
                    i+=1
            #yield query1, consult

if __name__ == '__main__':
    TwitterMRJob.run()