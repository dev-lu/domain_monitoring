#==============================================
# Search for new registered domains using urlscan.io API
# Author: https://github.com/dev-lu
#==============================================
from colorama import Fore, Back, Style
from prettytable import PrettyTable
import requests
import json
import dateutil.parser
import datetime


string = str(input('Enter Keyword:\n')).strip()

table = PrettyTable()
table.header = True
table.title = Style.BRIGHT + "Results" + Style.RESET_ALL
table.field_names = ["Domain", "Status code", "Certificate valid since", "TLS age", "ASN name", "Found at", "Days ago"]

url = f"https://urlscan.io/api/v1/search/?q=domain:{string}"
response = requests.get(url =  url)
response_json = json.loads(response.text)
if response.status_code == 200:
    for i in response_json["results"]:
        
        if "domain" in i["task"]:
            domain = i["task"]["domain"]
        else: domain = "N/A"
        
        if "status" in i["page"]:
            status = i["page"]["status"]
        else: status = "N/A"
        
        if "tlsValidFrom" in i["page"]:
            tls_from = i["page"]["tlsValidFrom"]
        else: tls_from = "N/A"
        
        if "tlsAgeDays" in i["page"]:
            tls_days = i["page"]["tlsAgeDays"]
        else: tls_days = "N/A"
        
        if "asnname" in i["page"]:
            asnname = i["page"]["asnname"]
        else: asnname = "N/A"
        
        if "time" in i["task"]:
            time = i["task"]["time"]
            time = dateutil.parser.isoparse(time).replace(tzinfo=None)
            delta = datetime.datetime.now() - time
        else: time = "N/A"
        table.add_row([domain, status, tls_from, str(tls_days) + " day(s)", asnname, time, str(delta.days) + " day(s)"])

    table.align = "l"  
    print(table)
else: print("Error while calling the API\n" + response.text)
