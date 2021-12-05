import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import folium


data = pd.read_csv('Dataset911.csv',low_memory=False)


#Compute -- What are the top 10 Zipcodes for 911 & Question 1: 
#Are Zipcodes 19446 and 19090 present ?
print("1. The top 10 Zipcodes for 911: ")
d1 = data['zip'].value_counts().head(10)
print(d1)

if (19446 in d1):
	print("19446 Present")
if (19090 in d1):
	print("19090 Present")
print("--------------------------------------------------------------")

#Compute -- What are the top 4 townships (twp) for 911 calls & Question 2: 
#Which of the following township are not present? -- LOWER POTTSGROVE,NORRISTOWN,HORSHAM,ABINGTON
print("2. The top 4 townships (twp) for 911 calls: ")
d2 = data['twp'].value_counts().head(4)
print(d2)
if ("LOWER POTTSGROVE" not in d2):
	print("LOWER POTTSGROVE not present")
if ("NORRISTOWN" not in d2):
	print("NORRISTOWN not present")
if ("HORSHAM" not in d2):
	print("HORSHAM not present")
if ("ABINGTON" not in d2):
	print("ABINGTON not present")
print("--------------------------------------------------------------")

#Compute -- Create new features & Question 3: 
#What is the most common Reason for a 911 call based on Reason Column? Which comes second
data[['reason','title']] = data.title.str.split(":",expand=True,)
d3 = data['reason'].value_counts().head(2)
#print(d3)
print("3. The two most common reasons for a 911 call are: ")
print(d3)
print("--------------------------------------------------------------")


#Compute -- Plot barchart using matplot for 911 calls by Reason & Question 4: 
#How can you plot the bars horizontally ?
#sns.countplot(x=data['reason'])
fig, ax = plt.subplots() 
data.reason.value_counts().plot.barh()
plt.xlabel('Count')
plt.ylabel('Reasons')
plt.show()

data['timeStamp'] = pd.to_datetime(data['timeStamp'])
data['date'] = [d.date() for d in data['timeStamp']]

data['Month'] = data['timeStamp'].apply(lambda x:x.month)
data['DayOfWeek'] = data['timeStamp'].apply(lambda x:x.dayofweek)

days = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
data['DayOfWeek']  = data['DayOfWeek'].map(days)

months = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
data['Month']=data['Month'].map(months)

#Do data manipulation & Question 5: 
#Which day got maximum calls for EMS and how many?
d = data[data['reason']=="EMS"]
d3 = d['DayOfWeek'].value_counts().head(1)
print("5. The day got maximum calls for EMS is: ")
print(d3)
print("--------------------------------------------------------------")


#Compute -- Create a countplot of the Day of Week column with the hue based of the
#Reason column & Question 6: On which day traffic calls were lowest ?
d4 = data[data['reason'] == "Traffic"]
d5 = d4['DayOfWeek'].value_counts().tail(1)
print("6. Traffic calls were lowest on: ")
print(d5)
print("--------------------------------------------------------------")

#Compute -- Create a countplot month wise -- Question 7: 
#Which month saw highest calls for fire?
d4 = data[data['reason'] == "Fire"]
d5 = d4['Month'].value_counts().head(1)
print("7. Fire cases were reported most in: ")
print(d5)
print("--------------------------------------------------------------")

#Compute -- Create Web Map for Traffic Calls & Question 8: 
#Why some areas seem to have lower or almost zero traffic calls? Hint: Zoom the map
data = data[data['reason'] =="Traffic"]
lon=list(data["lng"][0:1000])
lat=list(data["lat"][0:1000])
categoryName = list(data['title'][0:1000])
wDay = list(data['DayOfWeek'][0:1000])
map=folium.Map(location=[data["lat"].mean(),data["lng"].mean()],zoom_start=12,tiles='OpenStreetMap')
fg=folium.FeatureGroup(name="Traffic Locations")

def color_producer(day):
    if(day=="Monday"):
        return("green")
    elif(day=="Tuesday"):
        return("orange")
    elif(day=="Wednesday"):
        return("blue")
    elif(day=="Thursday"):
        return("darkpurple")
    elif(day=="Friday"):
        return("beige")
    elif(day == "Saturday"):
    	return("pink")
    else:
        return("red")
for lt,ln,name,wd in zip(lat,lon,categoryName,wDay):
    fg.add_child(folium.Marker(location=[lt, ln],popup=str(name),icon=folium.Icon(color=color_producer(wd))))
map.add_child(fg)

map.save('Traffic_1000.html')