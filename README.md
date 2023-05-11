# to create virtualenv using windows command promt
- to create virtualenv `python3 -m venv .proj-env`
- to activate virtualenv `.proj-env\Scripts\activate.bat`


# to intall required packages-
- open the file `notepad requirements.txt`
- to install all packages `pip install -r requirements.txt`
 
# Local run setup-
- if venv is not active `.proj-env\Scripts\activate.bat`
- run `python main.py`
- press CTRL button and click on `http://127.0.0.1:8080`
- to quit -> Press CTRL+C in the terminal

# Folder Structure

- `application` is where our application code is
- `db_directory` has the sqlite DB. 
- `Report&docs` - contains project report and yaml file.
- `static` - container for images.
- `templates` - Default flask templates folder
- `main.py` - python file to create the app.
- `requirements.txt` - contains all required packages to be installed to run the app.

```
├── application
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── controllers.py
│   ├── models.py
│   └── __pycache__
│       ├── __init__.cpython-310.pyc config.cpython-36.pyc
│       ├── api.cpython-310.pyc
│       ├── config.cpython-310.pyc
│       ├── controllers.cpython-310.pyc
│       ├── database.cpython-310.pyc
│       └── models.cpython-310.pyc
├── db_directory
│   └── database.sqlite3
├── Report&docs
│   |── openapi.yaml
|   └── Project_Report.pdf
├── static
├── templates
│   ├── add_card.html
│   ├── add_list.html
│   ├── alert.html
│   ├── base.html
│   ├── edit_card.html
│   ├── edit_li.html
│   ├── log.html
│   ├── summary.html
│   └── users.html
├── main.py
├── README.md
└── requirements.txt   
```