import requests
import re
import time
from termcolor import colored

# time to sleep between searches (5 seconds)
time_to_sleep = 5
# user agent for requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

companies_move_it_url = {}
def extract_urls_from_string(input_string):
    # Define the regex pattern to find URLs starting with /url?q=
    # pattern = r'/url\?q=(https?://[^&]+)'
    pattern = r'https://[^&?/]+/human\.aspx'
    
    # Find all occurrences of the pattern in the input string
    matches = re.findall(pattern, input_string)
    
    if matches:
        # Return the list of extracted URLs
        return matches
    else:
        return None


def get_companies_list():
	companies_list = []
	with open('companies.txt') as f:
		companies_list = f.read().splitlines()
		print("companies to look for using moveit software : ")
		print(colored(companies_list, 'blue'))
	return companies_list

def is_move_it_portal(url):
	move_it_portal="no"
	response_data =  requests.get(url, headers=headers)
	web_page_content = response_data.text
	if "moveit" in web_page_content:
		print("found!!!")
		move_it_portal = "yes"
	else:
		print("not found!")
	return move_it_portal

def get_company_moveit_url(companies_list):
	initial_url = "https://www.google.com/search?q=inurl%3A%2Fhuman.aspx"
	for company in companies_list:
		url = ''
		url += initial_url + "+" + company
		print("[+] looking for moveit urls for : " + company)
		response_data = requests.get(url, headers=headers)
		output = response_data.text
		all_urls = extract_urls_from_string(output)
		# dedup
		if not all_urls is None:
			all_urls = list(dict.fromkeys(all_urls))
			if len(all_urls) > 0:
				print(colored("[+] Found " + str(len(all_urls))) + " potential MoveIt portal URLs", "green")
				for url in all_urls:
					if not 'google.com' in url:
	#					if is_move_it_portal(url) == "yes":
						print(colored("[+]"+url, "green"))
		else:
			print("[-] No results found")
		print("#################################")
		print("sleeping for " + str(time_to_sleep) + " seconds..")
		time.sleep(time_to_sleep)

comp_list=get_companies_list()
get_company_moveit_url(comp_list)

