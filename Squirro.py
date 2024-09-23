from datetime import datetime
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
        self.schema = set()
        self.inc_column = None
        self.max_inc_value = None
    
    def connect(self, inc_column=None, max_inc_value=None):
        """
        Connect to the source and store incremental values if provided.
        """
        log.debug("Incremental Column: %r", inc_column)
        log.debug("Incremental Last Value: %r", max_inc_value)
        self.inc_column = inc_column
        self.max_inc_value = max_inc_value
    
    def disconnect(self):
        """Disconnect from the source."""
        # Nothing to do
        pass

    def flat_dictionary(self, d, parent_key='', sep='.'):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flat_dictionary(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                if all(isinstance(i, dict) for i in v):
                    for idx, item in enumerate(v):
                        items.extend(self.flat_dictionary(item, f"{new_key}[{idx}]", sep=sep).items())
                else:
                    items.append((new_key, v))
            else:
                items.append((new_key, v))
        return dict(items)
    
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
                'page': page
            }

            if self.inc_column == 'pub_date' and self.max_inc_value:
                date_obj = datetime.strptime(self.max_inc_value[:10], "%Y-%m-%d")
                begin_date = date_obj.strftime("%Y%m%d")
                params['begin_date'] = begin_date  
            
            response = requests.get("https://api.nytimes.com/svc/search/v2/articlesearch.json", params=params)

            if response.status_code == 200:
                data = response.json()
                articles = data['response']['docs']

                if not articles:
                    break

                for i in range(0, len(articles), batch_size):
                    batch = []
                    for article in articles[i:i + batch_size]:
                        flat_article = self.flat_dictionary(article)
                        self.schema.update(flat_article.keys())
                        batch.append(flat_article)
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
        #schema = [
        #    "title",
        #    "body",
        #    "created_at",
        #    "id",
        #    "summary",
        #    "abstract",
        #    "keywords",
        #]
        #return schema
        return sorted(list(self.schema))


if __name__ == "__main__":
    config = {
        "api_key": "Ts9vptT4oyQnKTNktURsz4AtNgLnyJOz",
        "query": "Silicon Valley",
    }
  
    source = NYTimesSource()

    # Use this if you want to use the connect function with inc_column and max_inc_value column defined
    #inc_column = 'pub_date'  # Example incremental column
    #max_inc_value = '2024-09-15T00:00:01+0000'  # Example last known value (start from Jan 1, 2023)
    #source.connect(inc_column=inc_column, max_inc_value=max_inc_value)
    
    source.connect()

    source.args = argparse.Namespace(**config)

    for idx, batch in enumerate(source.getDataBatch(10)):
        print(f"\n{idx} Batch of {len(batch)} items")
        for item in batch:
            print(f" - {item['_id']} - {item['headline.main']}")
            # Uncomment the lines below to print each flat article dictionary
            # for key, value in item.items():
            #     print(f"{key}: {value}")
            # print("\n")

    source.disconnect()
