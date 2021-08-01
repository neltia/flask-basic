from flask import Flask, render_template, request, send_file
from werkzeug import secure_filename
import os
app = Flask(__name__)
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #파일 업로드 용량 제한 단위:바이트

@app.errorhandler(404)
def page_not_found(error):
	app.logger.error(error)
	return render_template('page_not_found.html'), 404

#HTML 렌더링
@app.route('/')
def home_page():
	return render_template('home.html')

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
	else:
		return render_template('page_not_found.html')

#다운로드 HTML 렌더링
@app.route('/downfile')
def down_page():
	files = os.listdir("./uploads")
	return render_template('filedown.html',files=files)

#파일 다운로드 처리
@app.route('/fileDown', methods = ['GET', 'POST'])
def down_file():
	if request.method == 'POST':
		sw=0
		files = os.listdir("./uploads")
		for x in files:
			if(x==request.form['file']):
				sw=1
				path = "./uploads/" 
				return send_file(path + request.form['file'],
						attachment_filename = request.form['file'],
						as_attachment=True)

		return render_template('page_not_found.html')
	else:
		return render_template('page_not_found.html')

if __name__ == '__main__':
	#서버 실행
	app.run(host='0.0.0.0', debug = True)