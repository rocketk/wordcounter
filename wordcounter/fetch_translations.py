import codecs
import json
import urllib2
from copy import deepcopy
import ConfigParser


def fetch_translations_from_file(output_path="output/", words_file="filtered_words_of_the_book.txt"):
    trans_list = []
    dictionary_db_cache = read_dict_db()
    count_from_internet = 0
    with open(output_path + words_file) as f:
        for line in f:
            splited = line.split(",")
            word = splited[0]
            if word in dictionary_db_cache:
                trans = dictionary_db_cache[word]
            else:
                trans = fetch_translation_from_internet(word)
                dictionary_db_cache[word] = deepcopy(trans)
                count_from_internet += 1
            trans['count_in_book'] = splited[1]
            trans_list.append(trans)
            if len(trans_list) % 100 == 0:
                print "fetched {0} words".format(len(trans_list))
    print "all words are fetched successfully, total {0}, fetched from local cache {1}, fetched from internet {2}" \
        .format(len(trans_list), len(trans_list) - count_from_internet, count_from_internet)
    if count_from_internet > 0:
        print "rewritting fetched translationgs to local cache file"
        write_to_dict_db(dictionary_db_cache)
    return trans_list


def fetch_translation_from_internet(word):
    url = "http://dict.youdao.com/jsonresult?q={0}&keyfrom=deskdict.main&type=1&pos=-1&client=deskdict&id" \
          "=27ea057a1166e21b0&vendor=ynote.download&in=setup1_YoudaoDict_ynote.download&appVer=6.3.69.7015" \
          "&appZengqiang=0&abTest=5&le=eng&LTH=0".format(word)
    response = urllib2.urlopen(url)
    content = response.read()
    json_content = json.loads(content)
    # dict_content = {'basic': [], 'web': []}
    # for s in json_content['basic']:
    #     dict_content['basic'].append(unicode(s))
    # for s in json_content['web']:
    #     dict_content['web'].append(unicode(s))
    # return dict_content
    return json_content


def read_dict_db(dict_db_file="cache/translations_in_dict.json"):
    with codecs.open(dict_db_file, 'r', 'utf-8-sig') as f:
        words_dict = json.loads(f.read())
        return words_dict


def write_to_dict_db(words_dict, output_file='cache/translations_in_dict.json'):
    with codecs.open(output_file, 'w', "utf-8-sig") as f:
        f.write(json.dumps(words_dict, indent=4, ensure_ascii=False))


def write_to_js_file(trans_list, output_path="output/", output_file='data.js'):
    with codecs.open(output_path + output_file, 'w', "utf-8-sig") as f:
        f.write("var words = ")
        f.write(json.dumps(trans_list, ensure_ascii=False))


def list_to_dict():
    with codecs.open("cache/translations_in_list.json", 'r', "utf-8-sig") as f:
        translations_list = json.loads(f.read())
    print "read {0} words".format(len(translations_list))
    translations_dict = {}
    for word_dict in translations_list:
        if 'rq' in word_dict:
            translations_dict[word_dict['rq']] = word_dict
    with codecs.open("cache/translations_in_dict.json", 'w', "utf-8-sig") as f:
        f.write(json.dumps(translations_dict, indent=4, ensure_ascii=False))
    print "write {0} words".format(len(translations_dict))


if __name__ == '__main__':
    # words_file = sys.argv[1]
    # print "fetching translations..."
    # translations = fetch_translations_from_file(words_file)
    # print "writing file"
    # write_to_file(translations)
    # data = json.dumps(fetch_translation('windmill'), indent=4, ensure_ascii=False)
    # print data

    config = ConfigParser.RawConfigParser()
    config.read('config.properties')
    output_path = config.get("default", "output_path")
    trans_list = fetch_translations_from_file(output_path=output_path)
    write_to_js_file(trans_list, output_path=output_path)

    # list_to_dict()
