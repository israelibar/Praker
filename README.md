# Praker_ITC-Hackathon
Creating a service for "Parker" application, at ITC-Hackathon.

API:
* GET - lat (latitude), lng (longitude), time 
* Return - the average time to find parking in the closest point, in minutes (up to 10km)
* If the point if more than 10 km - return -1

*The API platform was deployed on ec2 platform (AWS), ROUTE: /get_avg_time*

Dataset:
https://www.kaggle.com/datasets/terenceshin/searching-for-parking-statistics-in-north-america

Geographic distance calculations were based on **geohash**, using pgh of pygeohash library.
