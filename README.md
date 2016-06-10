ODI PRE MATCH OUTCOME PREDICTION AND STRATEGY RECOMMENDATION SYSTEM
========

What is it?
-----------
This is a pre-match outcome prediction system that takes in historical match data to predict win or loss. We model the game using a subset of match parameters, using a K- nearest-neighbour clustering algorithms and SVM classifier. It also suggests player performance along with their preferred roles in the match.



Requirements:
-----------
* Python >= 3.0  
* Linux/Windows Operating System with atleast 1GB of RAM
* A browser to view the application

Dependencies:
-----------
cycler==0.10.0  
Flask==0.10.1  
itsdangerous==0.24  
Jinja2==2.8  
MarkupSafe==0.23   
matplotlib==1.5.1  
nltk==3.1  
numpy==1.10.4  
PyMySQL==0.7.2  
pyparsing==2.1.0  
python-dateutil==2.4.2  
pytz==2015.7  
scikit-learn==0.17  
scipy==0.17.0  
six==1.10.0  
Werkzeug==0.11.4  
wheel==0.24.0  

Setting Up:
-----------
* Install [Python](https://www.python.org/downloads/)  
* Install [Pip](http://python-packaging-user-guide.readthedocs.org/en/latest/install_requirements_linux/)  
* Copy code into a suitable project directory

* Install virtualenv: ``` $ [sudo] pip3 install virtualenv ```

* Setup virtualenv: ```$ cd /path/to/project/  && virtualenv env  && source  
                env/bin/activate```

* Install dependencies: ```$ pip3 install -r requirements.txt```

Running the script:
---
>Download score cards from [Howstat](http://www.howstat.com.au/) and store it in a directory named dataset/scorecard.  
>Dump the structured data onto the database.  
> Modify paths under code/core/config.py to the system path.

### 1. Data preprocessing:
```
$ python3 core/preprocessing/scorecard/extract.py
```
### 2. Run web application:
```
$ python3 app.py
```
##### Open browser and visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

