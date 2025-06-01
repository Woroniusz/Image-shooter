from src.Logger.logger import get_logger
from src.utils.Config import Config

logger = get_logger(__name__)

if __name__ == '__main__':
	try:
		# Load configuration from a file
		config: Config = Config('config.toml')
	except FileNotFoundError as e:
		logger.error(f'Configuration file not found: {e}')
		exit(1)
