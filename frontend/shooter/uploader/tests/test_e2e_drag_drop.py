import os

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shooter.settings')  # <- tutaj nazwa Twojego projektu
import django

django.setup()


class DragDropE2ETest(LiveServerTestCase):
	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-gpu')
		cls.browser = webdriver.Chrome(options=options)

	@classmethod
	def tearDownClass(cls) -> None:
		cls.browser.quit()
		super().tearDownClass()

	def setUp(self) -> None:
		self.browser.get(f'{self.live_server_url}/')
		# Wait for drop-area element to be present
		WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, 'drop-area')))
		# Inject the uploader script manually to avoid static file serving issues
		from django.conf import settings

		script_path = os.path.join(settings.BASE_DIR, 'uploader', 'static', 'uploader', 'script.js')
		with open(script_path) as f:
			script_content = f.read()
		# Append script to the page
		self.browser.execute_script(
			"const s = document.createElement('script');"
			"s.type = 'text/javascript';"
			's.text = arguments[0];'
			'document.body.appendChild(s);',
			script_content,
		)

	def test_drop_non_image_shows_alert(self) -> None:
		# Replace the alert to capture the message
		self.browser.execute_script('window.lastAlert = null; window.alert = function(msg){ window.lastAlert = msg; };')
		# Simulating the drop of a non-image file
		self.browser.execute_script(
			'var dt = new DataTransfer();'
			"dt.items.add(new File(['text'], 'test.txt', {type: 'text/plain'}));"
			"var event = new DragEvent('drop', { dataTransfer: dt, bubbles: true, cancelable: true });"
			"document.getElementById('drop-area').dispatchEvent(event);"
		)
		alert_text = self.browser.execute_script('return window.lastAlert;')
		self.assertEqual(alert_text, 'Proszę wybrać plik graficzny.')

	def test_drop_image_updates_preview(self) -> None:
		# Stub fetch and URL.createObjectURL
		self.browser.execute_script(
			'window.fetch = function(){ return Promise.resolve({'
			' ok: true,'
			" blob: () => Promise.resolve(new Blob([], {type: 'image/png'}))"
			'}); };'
			"window.URL.createObjectURL = function(){ return 'blob://fake'; };"
		)
		# Simulating the drop of an image file
		self.browser.execute_script(
			'var dt = new DataTransfer();'
			"dt.items.add(new File([''], 'a.png', {type: 'image/png'}));"
			"var event = new DragEvent('drop', { dataTransfer: dt, bubbles: true, cancelable: true });"
			"document.getElementById('drop-area').dispatchEvent(event);"
		)
		# Waiting for the image src to update
		WebDriverWait(self.browser, 5).until(
			lambda d: d.find_element(By.ID, 'preview').get_attribute('src') == 'blob://fake'
		)
		preview_src = self.browser.find_element(By.ID, 'preview').get_attribute('src')
		assert preview_src == 'blob://fake'
