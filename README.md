## Application Instructions

Clone the repo to your local machine by running the command:

```sh
git clone https://github.com/nikitow1/Youtube_DATA_API_Analysis_flask.git 
```

You must have python installed in your machine. After that, go into the folder with the project and create a virtual environment with the following command:

```sh
python3 -m venv venv
```

Active the respective environment by running:

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

## Google Colab Directory

Notebook file is in that directory





