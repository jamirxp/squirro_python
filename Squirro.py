import argparse
import logging
import requests

"""
Skeleton for Squirro Delivery Hiring Coding Challenge
August 2021
"""

log = logging.getLogger(__name__)

class NYTimesSource(object):
    """
    A data loader plugin for the NY Times API.
    """
    def __init__(self):
        pass
    
    def connect(self, inc_column=None, max_inc_value=None):
        log.debug("Incremental Column: %r", inc_column)
        log.debug("Incremental Last Value: %r", max_inc_value)
    
    def disconnect(self):
        """Disconnect from the source."""
        # Nothing to do
        pass

    def getDataBatch(self, batch_size):
        """
        Generator - Get data from source on batches.
        :returns One list for each batch. Each of those is a list of
        dictionaries with the defined rows.
        """
        # TODO: implement - this dummy implementation returns one batch of data
        #yield [
        #    {
        #    "headline.main": "The main headline",
        #    "_id": "1234",
        #    }
        #]
        
        api_key = self.args.api_key
        query = self.args.query
        page = 0
        
        while True:
            params = {
                'q': query,
                'api-key': api_key,
                'page': page,
            }

            response = requests.get("https://api.nytimes.com/svc/search/v2/articlesearch.json", params=params)

            if response.status_code == 200:
                data = response.json()
                articles = data['response']['docs']

                if not articles:
                    break

                for i in range(0, len(articles), batch_size):
                    batch = []
                    for article in articles[i:i + batch_size]:
                        flat = {
                            "web_url": article.get('web_url', ''),
                            "headline.main": article.get('headline', {}).get('main', 'No Headline'),
                            "headline.kicker": article.get('headline', {}).get('kicker', ''),
                            "abstract": article.get('abstract', ''),
                            "summary": article.get('summary', ''),
                            "keywords": article.get('keywords', []),
                            "_id": article.get('_id', '')
                        }
                        batch.append(flat)
                    yield batch
                
                page += 1 
            else:
                yield [] 

    def getSchema(self):
        """
        Return the schema of the dataset
        :returns a List containing the names of the columns retrieved from the
        source
        """
        schema = [
            "title",
            "body",
            "created_at",
            "id",
            "summary",
            "abstract",
            "keywords",
        ]
        return schema

if __name__ == "__main__":
    config = {
        "api_key": "Ts9vptT4oyQnKTNktURsz4AtNgLnyJOz",
        "query": "Silicon Valley",
    }
  
    source = NYTimesSource()
    
    # This looks like an argparse dependency - but the Namespace class is just
    # a simple way to create an object holding attributes.

    source.args = argparse.Namespace(**config)
    
    for idx, batch in enumerate(source.getDataBatch(10)):
        print(f"{idx} Batch of {len(batch)} items")
        for item in batch:
            print(f" - {item['_id']} - {item['headline.main']}")
