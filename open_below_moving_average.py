import requests
import os
import pprint

pprint.pprint(os.environ)
api_key = os.environ['FMPAPIKEY']

class FMPAPI:
  def __init__(self, api_key):
    self.apiKey = api_key
    self.urlBase = 'https://financialmodelingprep.com'
    self.urlPathRoot = '/api/v3'

  def getApiURLRoot(self):
    return self.urlBase + self.urlPathRoot

  def appendApiArgs(self, url, args = {}):
    args['apikey'] = self.apiKey
    pprint(args)
    kvpairs = []
    for k,v in args.items():
      kvpairs.append(k + '=' + v)
    url = url + '?' + '&'.join(kvpairs)

    return url

  def callAPIAndReturnJSON(self, url, args = {}):
    url = self.appendApiArgs(url, args)
    response = requests.get(url)
    response.raise_for_status()
    json_data = response.json()
    return json_data

  def realtime_quote(self, symbol):
    url = self.getApiURLRoot() + '/quote/' + symbol
    return self.callAPIAndReturnJSON(url)

  def historical_chart_5_min(self, symbol, start, end):
    url = self.getApiURLRoot() + '/historical-chart/5min/' + symbol
    return self.callAPIAndReturnJSON(url, {'from': start, 'to': end})

    

from pprint import pprint
api = FMPAPI(api_key)
#data = api.realtime_quote('META')
data = api.historical_chart_5_min('META', '2024-07-23', '2024-07-23')
#######

import pandas as pd
df = pd.DataFrame(data)


import plotly.graph_objects as go

fig = go.Figure(data=go.Scatter(go.Scatter(x=df['date'], y=df['close'])))
fig.show()
