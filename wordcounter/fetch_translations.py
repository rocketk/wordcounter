# coding=utf-8
import codecs
import json
import socket
import requests
from copy import deepcopy
import ConfigParser


def fetch_translations_from_file(output_path="output/", words_file="filtered_words_of_the_book.txt"):
    trans_list = []
    dictionary_db_cache = read_translations_db()
    count_from_internet = 0
    failed = []
    with open(output_path + words_file) as read_file, codecs.open("cache/translations_in_list.txt", "a", "utf-8") as db_file:
        for line in read_file:
            splited = line.split(",")
            word = splited[0]
            if word in dictionary_db_cache:
                trans = dictionary_db_cache[word]
            else:
                try:
                    trans = fetch_translation_from_internet(word)
                    dictionary_db_cache[word] = deepcopy(trans)
                    count_from_internet += 1
                    db_file.write(json.dumps(trans, ensure_ascii=False) + "\n")
                except socket.timeout, e:
                    failed.append(word)
                    continue
            trans['count_in_book'] = splited[1]
            trans_list.append(trans)
            if len(trans_list) % 100 == 0:
                print "fetched {0} words".format(len(trans_list))
    print "all words are fetched successfully, total {0}, fetched from local cache {1}, fetched from internet {2}, " \
          "failed {3}".format(len(trans_list), len(trans_list) - count_from_internet - len(failed),
                              count_from_internet, len(failed))
    # if count_from_internet > 0:
    #     print "rewritting fetched translationgs to local cache file"
    #     write_to_dict_db(dictionary_db_cache)
    return trans_list, failed


def fetch_translation_from_internet(word):
    url = "http://dict.youdao.com/jsonresult?q={0}&keyfrom=deskdict.main&type=1&pos=-1&client=deskdict&id" \
          "=27ea057a1166e21b0&vendor=ynote.download&in=setup1_YoudaoDict_ynote.download&appVer=6.3.69.7015" \
          "&appZengqiang=0&abTest=5&le=eng&LTH=0".format(word)
    try:
        response = requests.get(url)
        json_content = response.json()
        return json_content
    except socket.timeout, e:
        print "time out when fetching the word: " + word
        raise e
        # dict_content = {'basic': [], 'web': []}
        # for s in json_content['basic']:
        #     dict_content['basic'].append(unicode(s))
        # for s in json_content['web']:
        #     dict_content['web'].append(unicode(s))
        # return dict_content


def read_translations_db(dict_db_file="cache/translations_in_list.txt"):
    with codecs.open(dict_db_file, 'r', 'utf-8') as f:
        translations_dict = {}
        i = 0
        try:
            for line in f:
                i += 1
                translate_dict = json.loads(line, encoding="utf-8")
                if translate_dict and 'rq' in translate_dict:
                    translations_dict[translate_dict['rq']] = translate_dict
        except:
            print i, line
            raise
        return translations_dict


def write_to_dict_db(words_dict, output_file='cache/translations_in_dict.json'):
    with codecs.open(output_file, 'w', "utf-8") as f:
        f.write(json.dumps(words_dict, indent=4, ensure_ascii=False))


def write_to_js_file(trans_list, output_path="output/", output_file='data.js'):
    print("writing js file")
    with codecs.open(output_path + output_file, 'w', "utf-8") as f:
        f.write("var words = ")
        f.write(json.dumps(trans_list, ensure_ascii=False))


def tranform_file_from_list_to_dict():
    with codecs.open("cache/translations_in_list.json", 'r', "utf-8") as f:
        translations_list = json.loads(f.read())
    print "read {0} words".format(len(translations_list))
    translations_dict = {}
    for word_dict in translations_list:
        if 'rq' in word_dict:
            translations_dict[word_dict['rq']] = word_dict
    with codecs.open("cache/translations_in_dict.json", 'w', "utf-8") as f:
        f.write(json.dumps(translations_dict, indent=4, ensure_ascii=False))
    print "write {0} words".format(len(translations_dict))


def transform_file_from_dict_to_list():
    with codecs.open("cache/translations_in_dict.json", 'r', "utf-8") as f:
        translations_dict = json.loads(f.read())
    print "read {0} words".format(len(translations_dict))
    translations_list = []
    for key in translations_dict:
        translations_list.append(translations_dict[key])
    with codecs.open("cache/translations_in_list.txt", 'w', "utf-8") as f:
        for one in translations_list:
            f.write(json.dumps(one, ensure_ascii=False) + "\n")


if __name__ == '__main__':
    config = ConfigParser.RawConfigParser()
    config.read('config.properties')
    output_path = config.get("default", "output_path")
    trans_list, failed_list = fetch_translations_from_file(output_path=output_path)
    if not failed_list:
        write_to_js_file(trans_list, output_path=output_path)
    else:
        print "failed words: " + failed_list

        # transform_file_from_dict_to_list()
    # json_str = "{\"lang\": \"eng\", \"ltype\": \"ec\", \"uksm\": \"hə:'maiəni\", \"rq\": \"Hermione\", \"web\": [{\"Hermione\": [\"赫敏\", \"妙丽\", \"赫女星\"]}, {\"Hermione Corfield\": [\"赫敏·科菲尔德\"]}, {\"Hermione Grfrustrine\": [\"赫敏·格兰杰\"]}], \"usspeach\": \"Hermione&type=2\", \"basic\": [\"n. 赫尔迈厄尼（女子名）；希腊神话Menelzus 与helen 之女\"], \"ussm\": \"hə:'maiəni\", \"lname\": \"英汉翻译\", \"ukspeach\": \"Hermione&type=1\", \"sn\": -1, \"sm\": \"hə:'maiəni\", \"rec\": [], \"speach\": \"Hermione&type=1\", \"ver\": 1, \"sexp\": 0, \"type\": 2, \"oq\": \"hermione\", \"websame\": \"true\"}"
    # json_obj = json.loads(json_str, encoding="utf-8")
    # print json_obj
