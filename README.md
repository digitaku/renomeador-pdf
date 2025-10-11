pyinstaller --onefile main.py
pyinstaller --onefile --noconsole --add-binary "tesseract/tesseract:tesseract" --add-data "tesseract/tessdata:tesseract/tessdata" main.py
pip freeze > requirements.txt
pip install -r requirements.txt
