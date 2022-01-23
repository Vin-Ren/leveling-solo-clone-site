import os
import re
from flask import Blueprint, url_for, send_file, send_from_directory, render_template


solo_leveling = Blueprint('solo_leveling', __name__)
image_folder = './images'


def natural_key(string_):
	"""See https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/"""
	return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


def load(folder):
	chapters = os.listdir(folder)
	chapters.sort(key=lambda ch: natural_key(ch))

	chapters = [{'label':chapter, 'chapter': int(chapter.split()[1])} for chapter in chapters]
	return chapters

chapters = load(image_folder)


@solo_leveling.route('/')
def index():
	return render_template('index.html', chapters=chapters)


@solo_leveling.route('/images/chapter-<chapter>/<filename>')
def images(chapter, filename):
	return send_from_directory(f'{image_folder}/Chapter {chapter}', filename)


@solo_leveling.route('/mangas/chapter-<int:chapter>')
def chapterPage(chapter):
	images = os.listdir(f'{image_folder}/Chapter {chapter}')
	images.sort(key=lambda ch: natural_key(ch))
	return render_template('chapter_page.html', chapter=chapter, images=images, chapters=chapters)


@solo_leveling.route('/favicon.ico')
def favicon():
	return url_for('static', filename='favicons/192x192.png')

def setupWaitressLogger():
	logger = logging.getLogger('waitress')
	logger.setLevel(logging.INFO)
	handler = logging.FileHandler(filename=f'./logs.log', encoding='utf-8', mode='a')
	handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
	logger.addHandler(handler)


if __name__ == '__main__':
	from flask import Flask
	from argparse import ArgumentParser

	parser = ArgumentParser(__name__, description="Simple Web Interface To Read Leveling Solo Manhwa.")
	parser.add_argument('-p', '--port', dest='port', default='8080', type=int, help='Port to run the web server at. Default=80')
	parser.add_argument('-a','--host', dest='host', default='0.0.0.0', help='Address to run the web server at. Default=0.0.0.0')
	parser.add_argument('-t', '--threads', dest='threads', default=__import__('os').cpu_count()//2, 
						help='Threads to run waitress(if available). Default={}(Half of your cpu threads).'.format(__import__('os').cpu_count()//2))
	
	args = parser.parse_args()

	app = Flask(__name__)
	app.register_blueprint(solo_leveling)
	
	try:
		# Waitress isn't necessary.
		import waitress, logging
		setupWaitressLogger()
		waitress.serve(app, listen='{}:{}'.format(args.host, args.port), threads=args.threads)
	except (ImportError):
		app.run(host=args.host, port=args.port)