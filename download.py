import urllib3
import os
import logging

##Modify those two according to your necessary.
locations = ["USA", "Europe"]
years = [2020, 2019, 2018, 2017, 2016]


####################################################
##the maximum iteration of chapters 
MAX_CHAPTER = 1024

##the maximum iteration of papers in single chapter
MAX_ITEM = 1024

def rename_pdf_file(file_name):
    pass

##download single file
##return false if successful
def download_file(connection, type_s, download_url):
    ##try to connect to the website, if not success, skip the writing file step.
    rsp = connection.request("GET", download_url)
    if (rsp.status != 200):
        #logging.info("Failed to Download from {}".format(download_url))
        return  False

    logging.info("Successfully Downloading from {}".format(download_url))

    ##write to file, the name is the basename, such as 10_1.pdf
    file_name = type_s + "_" + os.path.basename(download_url)
    fd = open(file_name, "wb")
    fd.write(rsp.data)
    fd.close()

    rsp.close()

    return True


###helper function to change directory
def change_dir(dir_name):
    try:
        os.chdir(dir_name)
    except:
        logging.fatal("cannot chdir to dir {}".format(dir_name))
        sys.exit(-1)

##helper function to mkdir
##return false if not successful
def create_dir(dir_name):
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        s = "Folder {dir} already exists, skipping".format(dir = dir_name)
        logging.warning(s)
        return False

    ##success
    return True

##Wrapper to easier the loop downloading files
def download_file_wrapper(connection, year, location, chapter, type_s):
    #"http://events.dvcon.org/Europe/2018/proceedings/papers/01_3.pdf"
    str_fmt = "http://events.dvcon.org/{location}/{year:0d}/proceedings/{type_s}/{chapter:02d}_{item:0d}.pdf"

    valid = False ##incidate whether tis types in this chapter exits

    ##
    for item in range(1, MAX_ITEM):
        s = str_fmt.format(year = year,
                        location = location,
                        chapter = chapter,
                        item = item,
                        type_s  = type_s
                        )
        ret = download_file(connection, type_s, s)

        ##if any success
        if(ret):
            valid = True
        else:
            break

    return valid


## wrapper function to download each folder (usa_2020)
def download_dvcon_files(connection, year,  location):
    ##iterate each chpater, the type can be paper/silde/posters
    ##they are under diffrent folders
    for chapter in range(1, MAX_CHAPTER):
        chapter_valid = False
        for type_s in ["papers", "slides", "posters"]:
            ##if the first item in this type if not there, skip the entire type
            type_valid = download_file_wrapper(connection, year, location,
                chapter, type_s)
            if(not type_valid):
               continue 
            else:
                chapter_valid = True
        ##
        if(not chapter_valid):
            break

##main entry
def main(connection):
    cur_dir = os.path.abspath(os.path.curdir)

    ##TODO: split this function into smaller ones.
    for location in locations:
        for year in years:
            rel_path = location + "_{year:0d}".format(year = year)
            ##create a subfolder, format: Europe_2018, USA_2018
            dir_name = os.path.join(cur_dir, rel_path)

            ##if the foler exits, skip
            if(not create_dir(dir_name)):
                 continue

            ##down load the file
            change_dir(dir_name)
            
            ##if USA, url for location should be empty
            if(location == "USA"):
                location = ""

            ##do th real downloading.
            download_dvcon_files(connection, year,  location)

            ##go back.
            change_dir(cur_dir)
            ##

    ##happy ending
    logging.info("Enjoy DVCON!!!")

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    connection = urllib3.PoolManager()
    main(connection)
    connection.clear()
