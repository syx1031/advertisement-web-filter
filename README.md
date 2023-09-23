# Web Filter
 
### A project to filter websites that have advertisements.

## Prerequisites
* `pip install -r requirements.txt`
* Open your chrome manually and register `resource/ca.crt` as root certification (Read https://github.com/wkeeling/selenium-wire#certificates)

## Options

```
usage: main.py [-f {download_ad_image,ad_website_filter}] [-i WEB_LIST] [-o OUTPUT_PATH]
               [--filter FILTER_PATH]

Optional arguments:
  -f {download_ad_image,ad_website_filter},
                        Use crawl to download ad images or get websites list.
  -i WEB_LIST,          Path to the websites list to be filtered
                        (e.g. resource/tranco_6JNQX.csv).
  -o OUTPUT_PATH,       Path(directory) to write filtered list(ad images)
                        to, depending on option [-f].
  --filter FILTER_PATH, Path to the rules list(e.g. resource/easylist.txt).
```

## Authors
* **Yuxuan Shang** - [https://github.com/syx1031]
 
