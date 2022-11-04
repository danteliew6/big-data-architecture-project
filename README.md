Repository for IS459-Big Data Architecture group project<br>

Group members:
1. Dante Liew
2. Wang Wei Min
3. Jared Ng
4. Remus Chan

Copied over from Wei Min's github for my personal portfolio.

*Take note Scrapers do use the project files already made and change the configurations accordingly there!!! <br>

<h2>#Virtualenv guide</h2><br>
Creation<br>
1)virtualenv venv/.
<br>
<h2>Windows:</h2><br>
1)use command venv/Scripts/activate<br>
2)use command deactivate
<br>
<h2>MAC/Ubuntu:</h2>
1)use command source /venv/bin/activate<br>
2)use command deactivate
<br>
<h2>Use</h2><br> 
1)pip install -r requirements.txt


<h2>Files </h2> <br>
<ol>Selenium</ol>
    <p>Contains the files used for scraping monster.com using selenium</p>
<ol>Scrapy</ol>
    <p>Contains the folders for scraping the various websites</p>
<ol>Hadoop</ol>
    <p>Contains the consolidated parquet files arrgegated after the processing stage</p>
<ol>parquets</ol>
    <p>Contains the respective parquet files after each scraping </p>
<ol>djangoWebpage</ol>
    <p>Contains the files and settings for the Django webpages </p>
<ol>BDApages</ol>
    <p>Contains the files and settings for the visualisation of the data</p>
<ol>manage.py</ol>
    <p>the py file used to run the Django Application run via 'python manage.py runserver' </p>
