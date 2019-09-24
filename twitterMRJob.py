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
        for aux in hashtag:
            query = """
                    MERGE (person:User{id: '"""+user+"""'})-[:tweeted]->(n:Hashtag{hashtag:'"""+aux+"""'})
                    """
            graph.run(query)
            for aresta in hashtag:
                if aresta != aux:
                    query = """
                        MERGE (m:Hashtag{hashtag: '"""+aresta+"""'})-[:together]->(n:Hashtag{hashtag:'"""+aux+"""'})
                        """
                    graph.run(query)
        #yield user, hashtag

if __name__ == '__main__':
    TwitterMRJob.run()