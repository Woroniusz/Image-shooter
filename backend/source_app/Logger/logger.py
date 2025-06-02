import logging

# Konfiguracja domyślna: logowanie na poziomie INFO, format [czas] [poziom] nazwa: komunikat
logging.basicConfig(
	level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
)


def get_logger(name: str) -> logging.Logger:
	"""
	Zwraca logger o podanej nazwie.
	Przykład użycia: logger = get_logger(__name__)
	"""
	return logging.getLogger(name)
