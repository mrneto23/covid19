import http.client
import json
import pandas as pd
from pandas.io.json import json_normalize


class CovidTracker(object):
    """
    connect to TheVirusTracker API
    
    ...
    
    Methods
    ----------
    get_global_statistics()
        You will receive all of the current globally accumulated stats from Coronavirus Tracker.
        
    get_country_statistics(country)
        You will receive all of the current accumulated stats from Coronavirus Tracker for all of our indexed Country's.
        
    get_full_timeline()
        You will receive all of the timeline data from the Coronavirus Tracker.

    Returns
    -------
    The return will always be a dataframe ready to be used for analysis.
    
    """


    def consume_api_thevirustracker(self, url):
        conn = http.client.HTTPSConnection('thevirustracker.com')
        conn.request('POST', url)
        response = conn.getresponse()
        data = response.read()
        return(json.loads(data))


    def json_to_dataframe(self, df_json):
        return json_normalize(df_json)


    def get_global_statistics(self):
        url = '/free-api?global=stats'
        response = self.consume_api_thevirustracker(url)
        return self.json_to_dataframe(response['results'])


    def get_country_statistics(self, country):
        url = f'/free-api?countryTotal={country}'
        response = self.consume_api_thevirustracker(url)
        return self.json_to_dataframe(response['countrydata'])


    def get_full_timeline(self):
        url = '/timeline/map-data.json'
        response = self.consume_api_thevirustracker(url)
        dataframe = self.json_to_dataframe(response['data'])
        dataframe['date'] = pd.to_datetime(dataframe['date'], format="%m/%d/%y")
        dataframe['cases'] = dataframe['cases'].astype(int)
        dataframe['deaths'] = dataframe['deaths'].astype(int)
        dataframe['recovered'] = dataframe['recovered'].astype(int)
        dataframe.sort_values(by=['date'], inplace=True)
        return dataframe
