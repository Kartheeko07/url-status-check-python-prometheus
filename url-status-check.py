import requests
import time
import sys
import traceback
from prometheus_client import Gauge, start_http_server

# Creating metrics for Prometheus. We are using Gauge as it is the most suitable in this scenario as there is a frequent change in our metric
URL_UP = Gauge('sample_external_url_up', 'URL Up', ['url'])
URL_RESPONSE_MS = Gauge('sample_external_url_response_ms', 'Response Time', ['url'])

# Function to check the status of the url and return 1 if up and 0 if down
def check_url_status(url):
    try:
        # Getting the current request start time
        request_time = time.time() 
        # Using get method to get the URL Response, Here we are setting a minumum timeout of 5 seconds but that can configurable
        response = requests.get(url, timeout=5)
        # Determining the response time
        response_time = time.time() - request_time
        # Checking the status code of the response
        if response.status_code == 200:
            url_status = 1
        else:
            url_status = 0
    # In a scenario where there is a timeout
    except requests.exceptions.Timeout:
        # Using tracback for proper formatting and printing the exception
        traceback.print_exc()
        # Since there is a timeout service is considered as down
        url_status = 0
        # Set response time to Inf
        response_time = float('inf')    

    # Save the URL status as Prometheus output
    URL_UP.labels(url).set(url_status)
    # Save response time in milliseconds as Prometheus output
    response_time_ms = response_time * 1000
    URL_RESPONSE_MS.labels(url).set(response_time_ms)

    return url_status, response_time_ms

# Check the input list of URL's and returns the status output and response in milliseconds
def check_url(urls):
    url_status = {}
    url_response_ms = {}
    for url in urls:
        url_status[url] = check_url_status(url)[0]
        url_response_ms[url] = check_url_status(url)[1]
    return url_status, url_response_ms

if __name__ == '__main__':    
    urls = ["https://httpstat.us/503", "https://httpstat.us/200"]
    # print(check_url(urls))
    
    # Start up the server to expose the metrics.
    start_http_server(80) 
    while True:
        check_url(urls)
    
    
