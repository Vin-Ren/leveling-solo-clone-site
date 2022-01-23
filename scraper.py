import os
import requests
from bs4 import BeautifulSoup as bs



def soup_constructor(beautiful_soup, parser: str):
	def constructor(MarkUp, **kwargs):
		soup = beautiful_soup(MarkUp, parser, **kwargs)
		return soup
	return constructor


def make_soup(MarkUp, **kwargs):
	return soup_constructor(bs, 'html.parser')(MarkUp, **kwargs)


class Requester:
	def __init__(self):
		headers = {'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
		self.session = requests.Session()
		self.session.headers = headers

	def request(self, url, **kwargs):
		while True:
			resp = self.session.get(url, **kwargs)
			if resp.ok:
				return resp


class Chapter(Requester):
	def __init__(self, link):
		self.name = link.text
		self.images = []
		self.link = link
		self.url = link.get('href')
		self.site_content = ''
		super().__init__()

	def get_content(self):
		resp = self.request(self.url)
		self.site_content = resp.content
		return resp.content

	def get_images(self):
		content = self.site_content
		soup = make_soup(content)
		image_container = soup.find('article')
		images = [image for image in image_container.find_all('img')]
		self.images = images
		return images

	def save(self, folder_name):
		try:
			os.mkdir(os.path.join(folder_name, self.name.split(', ')[-1]))
		except:
			pass
		for pageNum, image in enumerate(self.images):
			print(f'Downloading Image #{pageNum+1}')
			try:
				image_content = self.request(image.get('src'), timeout=15).content

				with open(os.path.join(folder_name, self.name.split(', ')[-1], f"{pageNum}.{image.get('src').split('.')[-1]}"), 'wb') as file: # Anticipates different file extensions
					file.write(image_content)
			except KeyboardInterrupt:
				choice =  input(f"Keyboard Interrupt. Choices:\n[S]Skip Current Image\n[X]Stop Process\nChoice:").lower()
				if choice in ['s', 'skip', 'y', 'yes']:
					continue
				elif choice in ['x', 'stop', 'exit']:
					break
			except:
				print(f'Something is wrong with image #{pageNum+1}, Skipping Image.')
				continue


class Scraper(Requester):
	def __init__(self, image_folder=''):
		self.chapters = []
		self.image_folder = image_folder
		super().__init__()

		try:
			os.mkdir(self.image_folder)
		except:
			pass

	def scrape(self, limit=0, offset=0):
		print('Scraping Index...')
		self.get_index()
		print(f'Found {len(self.chapters)} Chapters.\n')
		print('Scraping Chapters...')
		self.get_chapters(offset=offset, limit=limit)

	def get_index(self):
		resp = self.request('https://levelingsolo.com')
		soup = make_soup(resp.content)

		chapter_list = soup.select_one('#ceo_latest_comics_widget-3')
		self.chapters = [Chapter(link) for link in chapter_list.find_all('a')]

	def get_chapters(self, offset=0, limit=0):
		# chapters = self.chapters[1:][::-1] # starts from latest ch-1 because latest contains only a timer.
		# Not valid anymore because its done.
		chapters = chapters[offset:limit] if limit else chapters[offset:] # if limit is 0, it will go to else.
		for chapter in chapters:
			print(f'Scraping: {chapter.name}')
			chapter.get_content()
			chapter.get_images()
			print('Downloading and saving images...')
			chapter.save(self.image_folder)
			print('\n')


if __name__ == '__main__':
	from argparse import ArgumentParser

	parser = ArgumentParser(__name__, description="Simple CLI app to scrape leveling solo manhwa chapters.")
	parser.add_argument('-f','--image-folder', dest='image_folder', default='images', help='Image folder to store the images.')
	parser.add_argument('-o', '--offset', dest='offset', default='0', type=int, help='Sets chapter scraping starting from chapter <offset>.')
	parser.add_argument('-l', '--limit', dest='limit', default='0', type=int, help='Sets scrape up to chapter <limit>.')
	
	args = parser.parse_args()

	s = Scraper(args.image_folder)
	s.scrape(limit=args.limit, offset=args.offset)
