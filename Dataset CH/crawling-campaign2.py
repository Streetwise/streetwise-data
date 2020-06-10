from pymapillary import Mapillary
from pymapillary.utils import *
import wget
import  libgeohash as gh
import datetime
from dotenv import load_dotenv
import os
import cv2
import image_processing as imgp


def convetBBoxtoMapillary(geohash):
    """
    Converts a geohash into a string  representing the bounding box coordinates in this order:
        Args:
            geohash (string):Geohash whose bounding box we want to obtain e.g. u0qj9

        Return:
            (string): bounding box  coordinates string in format West,South,East,North
    """
    gh_bbox = gh.bbox(geohash)
    return str(gh_bbox["w"])+","+str(gh_bbox["s"])+","+str(gh_bbox["e"])+","+str(gh_bbox["n"])


def register_entry(image_keys, coord_list, key_canton, i, ir, image_angles, sequence_info):
    """
    Downloads an image from mapillary given the image key and registers the entry in an existing  csv file.

           Args:
               image_keys (list):list containing mapillary iamge key from a sequence
               coord_list (list): list of coordinates corresponding to the images sent in image_keys
               key_canton (string): represents the canton where the image belongs, to be registered in the CSV file
               i (int): index to be added to the image name
               ir (int): image resolution
               image_angles (list): angles in which the images in image_keys were taken
               sequence_info (string): string containing  the mapillary key of the sequence, date when it was created
               and if it was taken as a panoramic image. This info is added to the csv for each image.
           Return:
               (int): the index used in the image name for the  images coming after this fucntion is executed

    """

    index_image=0
    while index_image + 16 < len(image_keys):
        flag=download_image_by_key(image_keys[index_image], ir, "im2/img" + str(i) + ".jpg")
        if not flag:
            myfile = open("data/crawling2.csv", "a")
            image_name="img" + str(i) + ".jpg"
            line=",".join([image_keys[index_image], image_name, key_canton, str(coord_list[index_image][1]),
                           str(coord_list[index_image][0]), str(image_angles[index_image]), sequence_info+"\n"])
            myfile.write(line)
            myfile.close()
        index_image+= 15
        i+=1

    return i



# https://www.mapillary.com/developer/api-documentation/#retrieve-image-sources
def download_image_by_key(key, image_resolution=320, download_path=None):

    """Download a image by the key

    Args:
        key (string): Image key of the image you want to download.
        image_resolution (int): Resolution of the image you want to download.
        download_path (string): The download path of the file to download.

    Return:
        (boolean): True if the download is sucessful (for now)

    """

    # Check the image_resolution argument and create the url to download
    if image_resolution == 320:
        url = "https://images.mapillary.com/" + key + "/thumb-320.jpg"
    elif image_resolution == 640:
        url = "https://images.mapillary.com/" + key + "/thumb-640.jpg"
    elif image_resolution == 1024:
        url = "https://images.mapillary.com/" + key + "/thumb-1024.jpg"
    elif image_resolution == 2048:
        url = "https://images.mapillary.com/" + key + "/thumb-2048.jpg"

    # Use the wget library to download the url
    filename = wget.download(url, download_path)
    img = cv2.imread(download_path)


    if  imgp.isBlurred(img,500) or imgp.isDark(img,60):
        os.remove(download_path)
        return True
    elif imgp.hasVehicles(download_path):
        os.remove(download_path)
        return True
    return False

##*****************Main program ***************


#Geohashes of the crawled areas
#old: "jd0c","jd36", "j6nx", "jd36", "jd28", "j6sd","j6vv", "j9b3", "j3yz", "j9g4", "j94u", "jd2j", "jd86", "j6fq", "j4x0", "jdqy"
#old "u0qk8tk", kc7h, kce8, tv3h, wt7, u0mtx5, u0mgtj8, u0mgtj8, u0qh3f2, u0qh3g2, u0qh3g2

#add geohashes as needed 
gh_cantons={"ZH": {"area_gh":"u0q", "suffix":["jd0c", "jd36", "jd36","jd28","j6sd", "j6vv", ]},
            "SH":{"area_gh":"u0q", "suffix":["pk7m", "pkds"]},
            #"LU":{"area_gh":"u0mg", "suffix":["tn", "th","tv","t7","ws"]},
            #"ZG":{"area_gh":"u0qh", "suffix":[ "3s","3f","3z","2t"]}
            #"SG":{"area_gh":"u0qt","suffix":["v3","v7","tx","ub","vu","su"]},
            #"SZ":{"area_gh":"u0q5", "suffix":["kz", "s3", "mn","7g","ds"]},

            #"TG":{"area_gh":"u0qq", "suffix":["d3", "df", "9f","em","3v"]},
            #"AG":{"area_gh":"u0m" ,"suffix":["tx5","tx1","txf","vd4", "vdj","v9e"]},
            #"RU":{"area_gh":"", "suffix":["u0mufst", "u0mu27","u0qw9m","u0qn66","u0qhnr","u0myj4","u0qkfy","u0qssc","u0qwt7", "u0qwq9","u0qv90","u0qjq7"]}
            }

#We get images from 2015 onwards
start_date=datetime.datetime(2015,1,1)

# Create a Mapillary Object
load_dotenv()
key = os.getenv("MAPILLARY_KEY")

map = Mapillary(key)

#Used to name images
i = 3261
image_resolution=1024


for key_canton in gh_cantons.keys():
    area_canton=0
    while area_canton < len(gh_cantons[key_canton]["suffix"]):
        gh_urban=gh_cantons[key_canton]["area_gh"]+ gh_cantons[key_canton]["suffix"][area_canton]
        #gh_urban = geohash_compl[area_canton]
        print(gh_urban)
        gh_box_map=convetBBoxtoMapillary(gh_urban)
        #we query sequences because we don't want many similar images in one area
        raw_json = map.search_sequences(bbox=gh_box_map, start_time=start_date)

        # every feature is a sequence of pictues
        sequence_list = raw_json["features"]

        for feature in sequence_list:
            image_keys = feature["properties"]["coordinateProperties"]["image_keys"]
            coordinates= feature["geometry"]["coordinates"]
            image_angles= feature["properties"]["coordinateProperties"]["cas"]
            sequence_info=','.join([feature["properties"]["key"],feature["properties"]["captured_at"],str(feature["properties"]["pano"])])
            i=register_entry(image_keys, coordinates, key_canton, i, image_resolution, image_angles, sequence_info)

        area_canton+=1

print("End of crawling")


