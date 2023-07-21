sts.get(url, headers=headers)
                output = response_data.text
#               print(output)
#               text_file = open("test.txt", "w")
#               text_file.write(output)
#               text_file.close()
                all_urls = extract_urls_from_string(output)
                # dedup
                if not all_urls is None:
                        all_urls = list(dict.fromkeys(all_urls))
                        if len(all_urls) > 0:
                                for url in all_urls:
                                        if not 'google.com' in url:
        #                                       if is_move_it_portal(url) == "yes":
                                                print(url)
                else:
                        print("[-] No results found")
                print("#################################")
                print("sleeping for " + str(time_to_sleep) + " seconds..")
                time.sleep(time_to_sleep)

comp_list=get_companies_list()
get_company_moveit_url(comp_list)
