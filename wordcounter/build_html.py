import ConfigParser

import os
import shutil

if __name__ == '__main__':
    config = ConfigParser.RawConfigParser()
    config.read('config.properties')
    output_path = config.get("default", "output_path")
    # os.makedirs(output_path)
    shutil.copy("resources/jquery-1.12.4.min.js", output_path + "jquery-1.12.4.min.js")
    shutil.copy("resources/bootstrap.min.js", output_path + "bootstrap.min.js")
    shutil.copy("resources/bootstrap.min.css", output_path + "bootstrap.min.css")
    # shutil.copy("resources/jquery-ui.js", output_path + "jquery-ui.js")
    # shutil.copy("resources/jquery-ui.css", output_path + "jquery-ui.css")
    shutil.copy("resources/words_dictionary.html", output_path + "words_dictionary.html")
