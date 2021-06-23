# LEVELING SOLO CLONE SILE
## Intro
A Crappy clone from the levelingsolo.com site

|Pros                               |Cons              |
|---------                          |:------:          |
|No ads (reader template is cleaned)|Run it yourself.  |


## Usage Instructions
### Dependencies
Before scraping and starting the server, lets install the required dependencies.
Install dependencies with:
```bash
>pip install -r requirements.txt
```

> **Notes:**
> You may need to change `pip` to `pip3` depending on the OS you are using.
### To Scrape
Really, you just need to run the scraper.py file.
run it with: 
```bash
>python scraper.py 
```
#### Opts
Short option list
```
-f|--image-folder <foldername> | Sets where the images are going to be saved
                               | Default: 'images'
-o|--offset <offset>           | Sets chapter scraping starting offset
                               | Default: 0
-l|---limit <limit>            | Sets scrape up to chapter limit
                               | Default: 0
```
While the scraper is running, it would spout a decent info log.
> **Notes:**
> You may need to change `python` to `python3` depending on the OS you are using.

### Start The Server!
Now after you have scraped the images, you can finally start the server!
starting the server:
```bash
>python web.py
```
#### Opts
Short option list
```
-h|--host <host>		 	   | sets webserver host
                                           | Default: '0.0.0.0' A.K.A 'localhost'
-p|--port <port>			   | Sets webserver port
                                           | Default: 8080
```

You are now done! You can visit the site on localhost:8080 (localhost:8080 is the default host:port)
> **Notes:**
> You may need to change `python` to `python3` depending on the OS you are using.

## Development
This is just a random project I tried to do, I don't think others wasting their time on this (*mess*) code is worth their time.

---
### Messing Around
Anyways if you'd like to mess with this code, I think its still (*maybe*) readable enough for you.
**[Scraper.py](./scraper.py)** Doesn't seem appropriate to be read. **[Web.py](./web.py)** on the other hand, is very readable.
Oh yup, the **[Web.py](./web.py)** is made in Blueprint, if you want to port it, you can just import the blueprint like: 
```python
from flask import Flask
from solo_leveling_clone_site.web import solo_leveling

your_app_or_another_blueprint = Flask(__name__)

your_app_or_another_blueprint. \
register_blueprint(solo_leveling, \
                   url_prefix='/your_url_prefix_here') 
                   # Url prefix is optional
# Do Your stuff

```
And you should be good to go.

---
Thanks for reading! Have a good day :)
