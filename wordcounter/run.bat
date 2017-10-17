@echo off

pause

cd %~dp0

echo "python word_counter.py"
python word_counter.py >> output/run.log

echo "python filtrate_easy_words.py"
python filtrate_easy_words.py >> output/run.log

echo "python fetch_translations.py"
python fetch_translations.py >> output/run.log

echo "python build_html.py"
python build_html.py >> output/run.log

pause