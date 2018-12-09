# EC601-Mini-Project-3

Environment
---
This api is written and tested on Windows.  

### Basic Requirements  
#### 1. Python -- one of the following:  
CPython : 2.7 and >= 3.4  
PyPy : Latest version  
#### 2. MySQL Server -- one of the following:  
MySQL >= 5.5  
MariaDB >= 5.5  
#### 3. MongoDB -- one of the following:  
MongoDB: 2.6, 3.0, 3.2, 3.4, 3.6 and 4.0  

### Packages 
For users who run this api for the first time, please make sure you have following packages in your pc:  
#### 1. pymysql  
Please install this package with:  
```Bash
$ python -m pip install PyMySQL
```  
#### 2. pymongo  
It can also be installed by pip:
```Bash
$ python -m pip install pymongo
```
#### 3. tweepy  
A twitter api used in mini project 1:
```Bash
$ python -m pip install tweepy
```
Also, please make sure to replace following lines in test1.py with your own twitter api keys when testing the api:
```Python
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
```
#### 4. googlevision  
A google vision api used in mini project 1:
```Bash
$ python -m pip install google-cloud-vision
```
At meanwhile, please replace the following lines in api.py with your own json file, and put the json file in the current folder with api.py:
```Python
filename = self.path + "\My First Project-78c9371a06a3.json"
```
#### 5. ffmpeg
Please make sure you have installed the ffmpeg for making video, you can download it and find tutorial here:
https://www.ffmpeg.org/  

How To Use
---  
To use this api, there are few preparations need to be done at first.  
First, please open cmd, and input following commands to build a MySQL database for saving the data:  
``` Bash
mysql -u root -p  
mysql> create DATABASE twitter_db;
```  
Also create two tables in this database as following strcture:  
![Image text](https://github.com/xiangl18/EC601-Mini-Project-1/blob/EC601-mini_project-3/mini_project3_api/imgs/mysql.PNG)  
In this case I use Navicat, a GUI for MySQL database, which can be downloaded here:  
https://www.navicat.com/en/download/navicat-for-mysql  
You can also build tables by using following commands:  
``` Bash
mysql> CREATE TABLE IF NOT EXISTS `mysql_data`(
   `time` VARCHAR(100) NOT NULL PRIMARY KEY,
   `record` VARCHAR(100) NOT NULL,
)ENGINE=InnoDB DEFAULT CHARSET=utf8;  

mysql> CREATE TABLE IF NOT EXISTS `mysql_label`(
   `twitter_id` VARCHAR(100) NOT NULL PRIMARY KEY,
   `label` VARCHAR(100) NOT NULL,
   `img_url` VARCHAR(220) NOT NULL,
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```   
As for MongoDB, the structure should be as follows:  
![Image text](https://github.com/xiangl18/EC601-Mini-Project-1/blob/EC601-mini_project-3/mini_project3_api/imgs/mongodb.PNG)  
In this case I use Robo 3T, a GUI for MongoDB database, which can be downloaded here:   
https://robomongo.org/download  
You can also build the database by inputing following commands:  
``` Bash  
> use twitter_database
```
You can then run the test1.py for testing functions in api.


