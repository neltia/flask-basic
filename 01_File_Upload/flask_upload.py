from flask import Flask, render_template, request
from werkzeug import secure_filename
import os
app = Flask(__name__)
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #파일 업로드 용량 제한 단위:바이트

#HTML 렌더링
@app.route('/')
def home_page():
	return render_template('home.html')

# 파일 리스트
@app.route('/list')
def list_page():
	file_list = os.listdir("./uploads")
	html = """<center><a href="/">홈페이지</a><br><br>""" 
	html += "file_list: {}".format(file_list) + "</center>"
	return html

#업로드 HTML 렌더링
@app.route('/upload')
def upload_page():
	return render_template('upload.html')

#파일 업로드 처리
@app.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		#저장할 경로 + 파일명
		f.save('./uploads/' + secure_filename(f.filename))
		return render_template('check.html')

#서버 실행
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug = True)