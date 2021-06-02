## Application Instructions

Clone the repo to your local machine by running the command:

```sh
git clone 
```

You must have python installed in your machine. After that, go into the folder with the project and create a virtual environment with the following command:

```sh
python3 -m venv venv
```

Active the the respective environment by running:

```sh
. venv/bin/activate
```

**Note:** It might be important to specify the environment you are considering when running this code in your IDE.

Install the project's dependencies with the following command. 

```sh
pip install -r requirements.txt
````

Before running the application set the Flask environment variables:

```sh
export FLASK_APP=main.py
export FLASK_ENV=development
```

Run Flask... RUN!!

```sh
flask run
```

## Database Integration:
For database run:

```sh
python3 csv_to_db.py 
```
Sqlite3 is used as database for simplicity.

## Regarding jupyter/colab notebook file

Initially all the scraping and view tracking were done in ipynb file because of colab's speed. 

## URL:
<http://localhost:5000/api/v1>

## Instruction for the filtered video by performance:
Filter the video by 'Very Good'/ 'Good'/ 'Average'/ 'Below Average'/ 'Bad'

## Task lists:

1. Using Youtube API (https://developers.google.com/youtube/v3/) scrapes channel videos with tags and stats. 

**Answer:** *Done in the endpoints/channel_video_stats and also in jupyter notebook*
   
2. Also you need to track changes of video stats every N minutes to see how videos are performing. Please pick the interval to scan stats which, according to you, is efficient and smart. You can hardcode channel ID in code, that’s not important.

**Answer:** *Done in the colab/jupyter notebook file (See *Checking video stat after some interval* section)*

3. Create a DB scheme and save scraped data. Please consider, that we will want to scan a lot of channels, so queries to aggregate and select data shouldn’t take long. Use any database you feel right. 

**Answer:** *Done in csv_to_db.py. As there is no restriction about the choice of database, I used sqlite3.*

4. Create mini API, where you can filter videos:
 a) By tags. 
 b) By video performance (first-hour views divided by channels all videos first-hour views median) 
   
**Answer:** *Done in endpoints/tags, endpoints/video_performance and also in jupyter notebook*

5. Bonus points for:

 i) pseudo algorithm for fetching as many youtube channels as possible. 
   
   **Answer:** *Done in endpoints/max_channels and also in jupyter notebook*


 ii) unit tests 
 
   **Answer:** *Tried PynGuin for it due to deadline, but it seems that more time will be needed for this unit test.*
   