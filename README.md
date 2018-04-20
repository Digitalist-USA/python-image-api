# python-image-api
Python Image API

An API for determining whether an image contains a cat.

- Endpoint: /is_cat
- Methods: GET, POST
- Parameters:
    - image_url: str (required)
    - nocache: bool (optional, default=False)

Response is a JSON object, e.g.:
```
{
  "message": "Image contains a cat",
  "result": true,
  "status": 200
}

```

## Developer setup

### Requirements
- Python 3.6
- Redis

### Setup

E.g., in a virtualenv:
```
cd [project root]
pip install -r requirements.txt

```
TODO: Docker ... setup?

### Running the app
Start Redis server with default port (6379).

Run Celery (in virtualenv) from the project root directory:
```
celery -A tasks worker --loglevel=info
```

Run the Flask app (in virtualenv) from the project root directory:
```
export FLASK_APP=start.py
flask run
```

### Try it out

e.g.
```
curl "localhost:5000/is_cat?image_url=https://images.pexels.com/photos/20787/pexels-photo.jpg"

curl -X POST "localhost:5000/is_cat?image_url=https://images.pexels.com/photos/20787/pexels-photo.jpg"
```


## To Do's

- Tests
- Health checks
- Properly configure logging, Celery, and so on
- Docker ... stuff
