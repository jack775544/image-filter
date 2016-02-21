from PIL import Image
import os
import datetime
import shutil
import Tkinter as tk
import tkFileDialog

"""Returns the date that an image was taken
path-> the path of the image
return: The date the image was taken as a string in format %Y:%m:%d %H:%M:%S"""
def get_date_taken(path):
    return Image.open(path)._getexif()[36867]

"""Gets all files in a folder with the '.JPG' extenstion
path -> the path of the folder
return: A list of the images """
def get_sub_files(path):
    r = []
    for root, subFolders, files in os.walk(path):
        for pic in files:
            if not pic.endswith("JPG"):
                continue
            imgpath = os.path.join(root, pic)
            pictime = get_date_taken(imgpath)
            pictime = datetime.datetime.strptime(pictime, "%Y:%m:%d %H:%M:%S")
            r.append((pic, pictime, root))
    return r

"""
Gets a folder an converts it to a format for the os library
folder -> a representation of a folder path
return: the folder
"""
def get_folder(folder):
    os.chdir(folder)
    return os.path.abspath(os.curdir)

"""
Gets the next highest directory in the folder tree
folder -> the folder to get the parent directory of
return: the parent directory of the folder
"""
def get_higher_dir(folder):
    os.chdir(folder)
    os.chdir("..")
    return os.path.abspath(os.curdir)

"""
Gets the date of monday of the week given
date -> datetime format of a certain date
return: the date of the monday of that week
"""
def get_monday(date):
    return date - datetime.timedelta(days=date.weekday())

"""
Gets the folder name of where the image needs to be placed
img -> the image that needs to be desigated
day -> weather the image is during the day. Night iff 1
return: the folder name where the image needs to be placed
"""
def get_designated_folder(img, day=0):
    time = img[1]
    root = img[2]
    if day == 1:
        return os.path.join(get_higher_dir(get_higher_dir(root)), "sorted", "night", "images " + get_monday(time).strftime("%Y %m %d"))
    else:
        return os.path.join(get_higher_dir(get_higher_dir(root)), "sorted", "day", "images " + get_monday(time).strftime("%Y %m %d"))

def main():
    root = tk.Tk()
    root.withdraw()
    print "Navigate to the unsorted folder..."
    folder = get_folder(tkFileDialog.askdirectory(initialdir="/", title="The root folder of the unsorted images"))
    print folder
    acknowledge = raw_input("press y then enter to continue: ")
    if acknowledge.strip().lower() != "y":
        print "exiting..."
        return
    print "continuing...\r"
    piclist = get_sub_files(folder)
    x = 0
    y = 0
    start_time = 0
    end_time = 0
    for pic in piclist:
        x = x + 1
        start_time = datetime.datetime.strptime(str(pic[1].year) + ":" + str(pic[1].month) + ":" + str(pic[1].day) + " 7:30:00" ,"%Y:%m:%d %H:%M:%S")
        end_time = datetime.datetime.strptime(str(pic[1].year) + ":" + str(pic[1].month) + ":" + str(pic[1].day) + " 16:30:00" ,"%Y:%m:%d %H:%M:%S")
        if (pic[1] < end_time) and (pic[1] > start_time):
            # good image options
            new_folder = get_designated_folder(pic)
            try:
                os.makedirs(new_folder)
            except:
                pass
            img_name = pic[1].strftime("%Y.%m.%d %H.%M.%S ") + pic[0]
            formatted_name = os.path.join(new_folder, img_name)
            shutil.move(os.path.join(pic[2], pic[0]), formatted_name)
            print "Moved Good Image: " + img_name
            y = y + 1
        else:
            # bad image options
            new_folder = get_designated_folder(pic, 1)
            try:
                os.makedirs(new_folder)
            except:
                pass
            img_name = pic[1].strftime("%Y.%m.%d %H.%M.%S ") + pic[0]
            formatted_name = os.path.join(new_folder, img_name)
            shutil.move(os.path.join(pic[2], pic[0]), formatted_name)
            print "Moved Bad Image: " + img_name
    print "\nTotal Images: " + str(x)
    print "Good Images: " + str(y)
    
if __name__ == "__main__":
    main()
