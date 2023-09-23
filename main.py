import time
import os
import sys
import getopt
import urllib.parse as urlparse
import pandas as pd
from seleniumwire import webdriver
import seleniumwire.undetected_chromedriver as uc
from adblockparser import AdblockRules

# import logging
# logging.basicConfig(level=logging.DEBUG)


class Engine:
    __engine = None

    def __init__(self, filter_path):
        with open(filter_path, 'r', encoding='utf-8') as f:
            rules_text = f.read()
        raw_rules = [line for line in rules_text.split('\n') if not line.startswith('!')]

        self.__engine = AdblockRules(raw_rules)

    def judge(self, judge_url):
        return self.__engine.should_block(judge_url)


if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "f:i:o:", longopts=["filter="])

    method = 0
    input_website_list = None
    output_file = None
    filter_file = None

    for opt_name, opt_value in opts:
        if opt_name == '-f':
            if opt_value == 'download_ad_image':
                method = 0
            elif opt_value == 'ad_website_filter':
                method = 1
        if opt_name == '-i':
            input_website_list = opt_value
        if opt_name == '-o':
            output_file = opt_value
        if opt_name == "--filter":
            filter_file = opt_value

    assert(input_website_list and output_file and filter_file)

    engine = Engine(filter_file)

    # result = engine.judge("https://ad/img/image.jpg")

    if method == 1:
        input_df = pd.read_csv(input_website_list, header=None)
        output_df = pd.DataFrame(columns=["order", "url"])

        last_length = 0

        for index in input_df.index:
            # if index < 829:
            #     continue
            url = input_df.iloc[index, 1]
            url_reg = urlparse.urlunparse(urlparse.urlparse(url, scheme="https"))

            print(">>>> %d : %s" % (index, url_reg))

            try:
                os.system('taskkill /im chromedriver.exe /F >> NUL 2>&1')
            except Exception as e:
                print("Error when trying to kill ChromeDriver")

            try:
                os.system('taskkill /im chrome.exe /F >> NUL 2>&1')
            except Exception as e:
                print("Error when trying to kill Chrome")

            try:
                options = uc.ChromeOptions()
                # options.add_argument('--headless')
                # options.add_argument('connection_timeout=15')
                # options.add_argument('--ignore-ssl-errors=yes')
                # options.add_argument('ignore-certificate-errors')
                # driver = webdriver.Chrome()
                driver = uc.Chrome(options=options, seleniumwire_options={})
                driver.get(url_reg)

            except Exception as e:
                print("Error when trying to open Chrome or navigate to target")
                continue
            else:
                time.sleep(15)

                msg = driver.page_source

                if "HTTP Status 404" in msg:
                    print("Error: HTTP Status 404")
                elif "502 Bad Gateway" in msg:
                    print("Error: 502 Bad Gateway")
                elif "403 Forbidden" in msg:
                    print("Error: 403 Forbidden")
                else:
                    reqs = driver.requests

                    for req in reqs:
                        if req.method == "GET" and engine.judge(req.url):
                            output_df.loc[len(output_df.index)] = [len(output_df.index) + 1, url]
                            break

                    length = len(output_df.index)
                    if length % 10 == 0 and length != last_length:
                        output_df.to_csv(output_file, index=False, header=False)
                        last_length = length

                driver.quit()

        output_df.to_csv(output_file, index=False, header=False)
