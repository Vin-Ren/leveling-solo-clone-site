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



if __name__ == '__main__':
	from flask import Flask

	# A small arg parser
	import sys.argv 
	from getopt import getopt
	host, port = '0.0.0.0', 8080
	opts, args = getopt(sys.argv[1:], 'h:p:', ['host=', 'port='])
	for opt, val in opts:
		if opt in ['-h', '--host']:
			host = val
		elif opt in ['-p', '--port']:
			port = int(val)

	app = Flask(__name__)
	app.register_blueprint(solo_leveling)
	app.run(host=host, port=port)