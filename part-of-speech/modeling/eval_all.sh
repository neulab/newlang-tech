for lang_code in `ls data`; do
python main.py --mode eval --lang $lang_code
done
