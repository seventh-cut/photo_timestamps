import sys
import os
import exifread
import datetime

option = sys.argv[1]
path_name = sys.argv[2]
test = 0
d = datetime.datetime(2011,1,1)

def open_file(file_name, mode):
    # Open image file for reading (binary mode)
    try:
        f = open(file_name, mode)
        return f
    except os.error:
        print ("File cannot open: %s" %file_name)
        return None
    
def set_date(file_name, stamp):
    global test
    if test == 0:
        os.utime(file_name,(stamp, stamp))
    else:
        print ("test == 1 !!! Dry run")

def pdf_func(file_name):
    global d
    f = open_file(file_name, 'rb')
    if f == None:
        return
    stamp = 0
    for line in f:
        if line.startswith(b"/CreationDate(D:"):
            d = line.split("(D:")[1].split(")")[0]
            try:
                stamp = int(d.strptime(str(date_str), "%Y%m%d%H%M%S").timestamp())
                print ("File %s stamp found" % file_name)
            except:
                pass
            break
        if (b"<xap:CreateDate>") in line:
            date_str = line.split(b"<xap:ModifyDate>")[1].split(b"</xap:ModifyDate>")[0]
            date_str = date_str.decode('utf-8')
            stamp = int(d.strptime(str(date_str), "%Y-%m-%dT%H:%M:%S%z").timestamp())
            #print ("File %s stamp found" % file_name)
            break
    else:
        print ("File %s stamp NOT found" % file_name)
        return
    set_date(file_name, stamp)

def jpg_func(file_name):
    f = open_file(file_name, 'rb')
    if f == None:
        return
    # Return Exif tags
    tags = exifread.process_file(f)

    for tag in tags.keys():
        if tag == 'EXIF DateTimeOriginal' or tag == 'Image DateTime':
            date_str = tags[tag]
            print ("Key: %s, value %s, file %s" % (tag, date_str, file_name))
            d = datetime.datetime(2011,1,1)
            stamp = int(d.strptime(str(date_str), "%Y:%m:%d %H:%M:%S").timestamp())
            try:
                set_date(file_name, stamp)
            except:
                print ("could not set date")
                pass
            break
    else:
        print("EXIT DateTimeOriginal not found in:", file_name)
        for tag in tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                print ("    Key: %s, value %s" % (tag, tags[tag]))


if __name__ == "__main__":

    ext_func = {
        "jpg": jpg_func,
        "pdf": pdf_func
    }

    if option == "-d":
        # Change all file within a directory
        os.chdir(path_name)
        flist = os.listdir()
    elif option == "-f":
        # Chnage a single file
        flist = (path_name,)
    elif option == "-l":
        # Change all file in a text list
        flist = open(path_name, "r")

    for file_name in flist:
        file_name = file_name.strip()
        try:
            file_ext = file_name.split(".")[-1]
        except:
            print ("File %s extension not known, skip" % file_name)
            continue
        #try:
        ext_func[file_ext.lower()](file_name)
        #except:
        #    print ("Could not process file %s" % file_name)
            
