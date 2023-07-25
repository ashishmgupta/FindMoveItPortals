import requests
import re
import time
from termcolor import colored
import random
import yaml
#from googleapiclient.discovery import build


from urllib3.exceptions import InsecureRequestWarning
# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

my_api_key= config["google_api_key"]
my_cse_id= config["google_cse_id"]

def get_a_random_user_agent_from_list():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3030.113 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3030.114 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3030.97 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3031.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3031.18 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3032.0 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3032.49 Safari/537.3"
    ]

    return random.choice(user_agents)

def get_random_header():
	random_user_agent =  get_a_random_user_agent_from_list()
	headers = {'User-Agent': random_user_agent}
	return headers

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res

def google_search2(query, api_key, cse_id):
	# Prepare the API request URL
	url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cse_id}&q={query}"

	# Send the API request
	response = requests.get(url)

	# Process the response
	if response.status_code == 200:
		search_results = response.json()
		print(search_results)
	# Now you can work with the search results JSON object.
	# You'll find the search results in `search_results['items']`.
	else:
		print("Error: Unable to fetch search results.")


# time to sleep between searches (5 seconds)
time_to_sleep = 5
#get_companies_list()# user agent for requests
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
	print(colored("[+] Looking for MoveIt.....", "green"))
	try:
		response_data =  requests.get(url, headers=get_random_header(), verify=False)
		web_page_content = response_data.text
		if "moveit" in web_page_content:
			move_it_portal = "yes"
		else:
			print("not found!")
	except:
		print(url + " not reachable")

	return move_it_portal

def get_company_moveit_url(companies_list):
	initial_url = "https://www.google.com/search?q=inurl%3A%2Fhuman.aspx"
	for company in companies_list:
		url = ''
		url += initial_url + "+" + company
		print("[+] looking for moveit urls for : " + company)
		response_data = requests.get(url, verify=False, headers=get_random_header())
		output = response_data.text
#		print(output)
#		text_file = open("test.txt", "w")
#		text_file.write(output)
#		text_file.close()
		all_urls = extract_urls_from_string(output)
		# dedup
		if not all_urls is None:
			all_urls = list(dict.fromkeys(all_urls))
			if len(all_urls) > 0:
				print(colored("[+] Found " + str(len(all_urls))) + " potential MoveIt portal URLs", "green")
				for url in all_urls:
					if not 'google.com' in url:
						if is_move_it_portal(url) == "yes":
							print(colored("[+]"+url, "green"))
		else:
			print("[-] No results found")
		print("#################################")
		print("sleeping for " + str(time_to_sleep) + " seconds..")
		time.sleep(time_to_sleep)

#comp_list=get_companies_list()
#get_company_moveit_url(comp_list)


def get_all_search_results(api_key, search_engine_id, query, num_results):
    all_formatted_urls = []
    start_index = 1
    while len(all_formatted_urls) < num_results:
        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}&start={start_index}&num={min(10, num_results - len(all_formatted_urls))}"
        response = requests.get(url)
        if response.status_code == 200:
            search_results = response.json()
            if 'items' in search_results:
                for item in search_results['items']:
                    if 'formattedUrl' in item:
                        formatted_url = item['formattedUrl']
                        formatted_url_without_query = formatted_url.split('?')[0]
                        all_formatted_urls.append(formatted_url_without_query)
            start_index += len(search_results.get('items', []))
        else:
            print("Error: Unable to fetch search results.")
            print(response.text)
            break

    return all_formatted_urls


def get_all_search_results_via_google_api(api_key, search_engine_id, company):
	all_formatted_urls = []
	#url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q=inurl%3A%2Fhuman.aspx+{company}"
	url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q=inurl:/human.aspx+{company}"
	print(url)
	#print(get_random_header())
	#return 
	response = requests.get(url, headers=headers, verify=False)
	if response.status_code == 200:
		search_results = response.json()
		if 'items' in search_results:
			for item in search_results['items']:
				if 'formattedUrl' in item:
					formatted_url = item['formattedUrl']
					formatted_url_without_query = formatted_url.split('?')[0]
					print(colored("[+] Found URL "+ formatted_url_without_query, "green"))
					if is_move_it_portal(formatted_url_without_query) == "yes":
						print(colored("[+] Potential MoveIt URL : "+ formatted_url_without_query, "green"))
						all_formatted_urls.append(formatted_url_without_query)
				else:
					print("Error: Unable to fetch search results.")
					print(response.text)
					break
	return all_formatted_urls



#resp = google_search2("inurl%3A%2Fhuman.aspx+fiserv", my_api_key, my_cse_id)
# resp=get_all_search_results(my_api_key,my_cse_id,"inurl%3Aashishmgupta",4)
#print(resp)

def get_all_companies_data():
	companies_list = get_companies_list()
	for company in companies_list:
		print("[+] looking for moveit urls for : " + company)
		resp=get_all_search_results_via_google_api(my_api_key,my_cse_id,company)
		if len(resp) > 0:
			print(resp)
		else:
			print("No results found")


#get_all_companies_data()

comp_list=get_companies_list()
get_company_moveit_url(comp_list)
