import requests
from datadog import initialize, api
import time

class Stock:
	name = ''
	symbol = ''
	price = 0

def getStocks():
	stocks = []

	with open("stocks.txt", "r") as filestream:
		for line in filestream:
			currentline = line.split(",")
			stock = Stock()
			stock.name = currentline[0].rstrip()
			stock.symbol = currentline[1].rstrip()
			stocks.append(stock)
	return stocks

def getStockPrice(aStock):
	URL = "https://api.iextrading.com/1.0/stock/"+aStock.symbol+"/price"
	r = requests.get(url = URL)
	data = r.json()
	aStock.price = data

def sendMetricToDD(aStock):
	options = {
		'api_key': '2941097c17d0de885520f96439be776b',
		'app_key': '50cc6a742a2d7f3cfcda99a54e8bc932ced548c7'}

	initialize(**options)

	price = float(aStock.price)	

	#print "Sending Metric [stock.price] Points ["+str(aStock.price)+"] Tags [" +aStock.symbol+ "]"

	tag = ["symbol:%s" % (aStock.symbol)]

	api.Metric.send(metric='stock.price', points=price, tags=tag)

def main():
	stocks = getStocks()

	i=0
	while(i<len(stocks)):
		getStockPrice(stocks[i])
		#print "Stock ["+stocks[i].name+"] Symbol ["+stocks[i].symbol+"] Price ["+str(stocks[i].price)+"]"
		sendMetricToDD(stocks[i])
		#time.sleep(3)
		i=i+1
		
main()


