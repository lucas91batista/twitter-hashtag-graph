from mrjob.job import MRJob
from mrjob.step import MRStep
import json

class RankHashtag(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_tweet,
                   reducer=self.reducer_count_hashtag),
            MRStep(reducer=self.reducer_rank)
        ]

    def mapper_get_tweet(self, _, line):
        line = json.parse(line)
        tweet = line['text']
        words = tweet.split(' ')
        for hashtag in words:
            hashtag = hashtag.replace(' ','')
            if "#" in hashtag:
                yield hashtag, 1

    def reducer_count_hashtag(self, key, values):
        yield str(sum(values)).zfill(5), key
        
    def reducer_rank (self, count, hashtags):
        for item in hashtags:
            yield item, count

if __name__ == '__main__':
    RankHashtag.run()