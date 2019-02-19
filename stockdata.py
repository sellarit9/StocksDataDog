import requests
from datadog import initialize, api
import time, json

options = {}

class Stock:
	name = ''
	symbol = ''
	price = 0
	alertPrice = 0

def setupApi():
        options = {
        'api_key': '2941097c17d0de885520f96439be776b',
        'app_key': '50cc6a742a2d7f3cfcda99a54e8bc932ced548c7'
        }

        initialize(**options)


def getStocks():
        stocks = []

        with open("stocks.txt", "r") as filestream:
                for line in filestream:
                        currentline = line.split(",")
                        stock = Stock()
                        stock.name = currentline[0].rstrip()
                        stock.symbol = currentline[1].rstrip()
                        stock.alertPrice = currentline[2].rstrip()
                        stocks.append(stock)
        return stocks

def getStockPrice(aStock):
	URL = "https://api.iextrading.com/1.0/stock/"+aStock.symbol+"/price"
	r = requests.get(url = URL)
	data = r.json()
	aStock.price = data

def sendMetricToDD(aStock):

	price = float(aStock.price)	

	#print "Sending Metric [stock.price] Points [" + aStock.price + "] Tags [" +aStock.symbol+ "]" 

	tag = ["symbol:%s" % (aStock.symbol)]
	api.Metric.send(metric='stock.price', points=price, tags=tag)

def createAlert(aStock):
	tags = ["stocks"]

	recov = int(aStock.alertPrice)-2

	options =  {
		"notify_audit": False,
		"locked": False,
		"timeout_h": 0,
		"new_host_delay": 300,
		"require_full_window": True,
		"notify_no_data": False,
		"renotify_interval": "0",
		"escalation_message": "",
		"include_tags": True,
		"thresholds": {
			"critical": aStock.alertPrice,
			"critical_recovery": recov
		}}

	api.Monitor.create(
	    type="query alert",
	    query="avg(last_5m):avg:stock.price{symbol:"+aStock.symbol+"} > "+aStock.alertPrice,
	    name=aStock.symbol+" is over $"+aStock.alertPrice,
	    message=aStock.symbol+" Stock Price is over $"+aStock.alertPrice+" @sellarit9@gmail.com @tre.sellari@datadoghq.com",
	    tags=tags,
	    options=options
	)	

def checkForExistingMonitor(aStock):
	hold = api.Monitor.search()

	if aStock.symbol+' is over $'+aStock.alertPrice not in str(hold):
		print("Creating Monitor for " + aStock.symbol)
		createAlert(aStock)


def main():
	stocks = getStocks()

	setupApi()

	i=0
	while(i<len(stocks)):
		s = stocks[i]
		print(s.symbol)
		getStockPrice(stocks[i])
		#print "Stock ["+stocks[i].name+"] Symbol ["+stocks[i].symbol+"] Price ["+stocks[i].price+"]"
		sendMetricToDD(stocks[i])
		#time.sleep(3)
		i=i+1

main()

#URL = "https://api.iextrading.com/1.0/stock/msft/price" 

#r = requests.get(url = URL)

#data = r.json()

#print data



