# Mapillary Crawling for Streetwise
Script for the dataset creation for Streetwise. 

This script crawls Mapillary and retrieves images belonging to Geohashes over Switzerland

## Dependencies 
- [pymapillary](https://github.com/khmurakami/pymapillary)
- [libgeohash](https://pypi.org/project/libgeohash/)
- [dotenv](https://pypi.org/project/python-dotenv/)

# Mapillary Crawling for Streetwise Campaign 2

This script analyzes the images before registering them in the CSV file. It discards them when they are too blurry, too dark or bright and depending also in the number of cars detected (i.e., if the image has more than 3 cars, then it's discarded)

It is necessary to download RetinaNet weights for the object detection: https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/resnet50_coco_best_v2.0.1.h5
