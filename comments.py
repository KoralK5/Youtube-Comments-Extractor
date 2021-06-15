from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
from os import system
import io

def grab(url, duration, curr, total):
	options = webdriver.ChromeOptions(); options.add_argument("--headless")
	
	try:
		driver = webdriver.Chrome(ChromeDriverManager().install(), options=options); driver.get(url); sleep(1)
	except:
		return ['']
	
	prevHeight = 0
	for scroll in range(duration):
		system('cls')
		print('PROGRESS\n')
		print(f'Total - {int((curr/total+(scroll/duration)*(1/total))*10) * "⬜"}▶️  {int((curr/total+(scroll/duration)*(1/total))*100)}%')
		print(f'Link  - {int(scroll/duration*10) * "⬜"}▶️  {int(scroll/duration*100)}%')
		
		height = driver.execute_script("""
				function getActualHeight() {
					return Math.max(
						Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
						Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
						Math.max(document.body.clientHeight, document.documentElement.clientHeight)
					);
				}
				return getActualHeight();
				""")
		driver.execute_script(f"window.scrollTo({prevHeight},{prevHeight + 200})"); sleep(0.1)
		prevHeight += 200
	
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	driver.quit()

	return [x.text for x in soup.select("#content #content-text")]

if __name__ == "__main__":
	duration = int(input('Extract duration in seconds: ')) * 10
	print('\nPaste in youtube links (enter ` to stop):\n')
	
	urls = []
	while '`' not in urls:
		urls.append(input())
	
	size = len(urls[:-1])
	for url in range(size):
		comments = grab(urls[url], duration, url, size)
		f = io.open('comments.csv', 'a', encoding="utf-8")
		f.write('»'.join(comments) + '»')

	print('\nCOMPLETE!')
