@echo off

pause

cd %~dp0

echo "python word_counter.py"
python word_counter.py

echo "python filtrate_easy_words.py"
python filtrate_easy_words.py

echo "python fetch_translations.py"
python fetch_translations.py

echo "python build_html.py"
python build_html.py

pause