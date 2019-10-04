from mrjob.job import MRJob
from mrjob.step import MRStep
import json
import re

class RankHashtag(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_tweet,
                   reducer=self.reducer_count_hashtag),
            MRStep(reducer=self.reducer_rank)
        ]

    def mapper_get_tweet(self, _, line):
        line = json.loads(line)
        tweet = line['text']
        #Removing control characters \n \r \t
        tweet = re.sub(r'[\n\r\t]', ' ', tweet)
        words = tweet.split(' ')
        for hashtag in words:
            if "#" in hashtag:
                #Removing unicodes
                hashtag = hashtag.encode('ascii','ignore')
                hashtag = hashtag.decode("ascii")
                hashtag = hashtag.strip()
                #Converting to lowercase
                hashtag = hashtag.lower()
                #Removing non alphanumeric characters
                hashtag = ''.join(c for c in hashtag if c.isalnum() or c =='#')
                yield hashtag, 1

    def reducer_count_hashtag(self, key, values):
        yield str(sum(values)).zfill(5), key
        
    def reducer_rank (self, count, hashtags):
        for item in hashtags:
            yield item, count

if __name__ == '__main__':
    RankHashtag.run()
