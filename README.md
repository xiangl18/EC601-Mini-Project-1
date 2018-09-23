# EC601-Mini-Project-1

How To Use
---
For users who run this project for the first time:  
1. Please dowload all files to one folder you have created, then add your own google vision credential file(json) to this folder, and edit the line 12 in googlevision.py, change the .json to your own file name.  

2. Edit the get.py, change the twitter api as follow to your own:
```python
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
```

3. Please run the main.py, then there will be instructions as:  
```python
Please inpute path:  
Please inpute frame_rate: 
```
and
```python
Please input a searching keyword:
```
if you choose the search method. Please input them by order, then you will get the images and the video made by these images in the folder you have input before.  

There is a demo video in this project folder.<br><br>

Upgrade 9.23
---
Made some modification and upgrades:  
1. Fix the fail to add google vision key to the environment bug in the googleVision.py.  

2. Add warning function for the get.py in case the twitter developer key is invalid, and add warnings for other exceptions.  

3. Add instruction for inputing frame rate.
