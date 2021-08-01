import webbrowser

def blogopen(url):
	link = 'https://blog.naver.com/%s'
	blog = link % (url)
	webbrowser.open(blog)