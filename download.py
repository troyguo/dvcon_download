import urllib3
import os
import logging

#"http://events.dvcon.org/Europe/2018/proceedings/papers/01_3.pdf"
temp_str = "http://events.dvcon.org/{location}/{year:0d}/proceedings/{type_s}/{chapter:02d}_{item:0d}.pdf"

MAX_CHAPTER = 30
MAX_ITEM = 30

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

def main(connection):
    locations = ["USA", "Europe"]
    years = [2019] 2018, 2017, 2016]
    cur_dir = os.path.abspath(os.path.curdir)

    ##TODO: split this function into smaller ones.
    for location in locations:
        for year in years:
            rel_path = location + "_{year:0d}".format(year = year)
            ##create a subfolder, format: Europe_2018, USA_2018
            dir_name = os.path.join(cur_dir, rel_path)
            try:
                os.mkdir(dir_name)
            except FileExistsError:
                s = "Folder {dir} already exists, skipping".format(dir = dir_name)
                logging.warning(s)
                continue

            ##
            try:
                os.chdir(dir_name)
            except:
                sys.exit("cannot chdir to dir {}".format(dir_name))

            ##if USA, url for location should be empty
            if(location == "USA"):
                location = ""

            for chapter in range(1, MAX_CHAPTER):
                for type_s in ["papers", "slides", "posters"]:
                        for item in range(1, MAX_ITEM):
                            s = temp_str.format(year = year,
                                                location = location,
                                                chapter = chapter,
                                                item = item,
                                                type_s  = type_s
                                                )
                            ret = download_file(connection, type_s, s)
                            if(not ret):
                                break

            ##chdir back.
            try:
                os.chdir(cur_dir)
            except:
                sys.exit("cannot chdir to dir {}".format(dir_name))
            ##

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    connection = urllib3.PoolManager()
    main(connection)
    connection.clear()
