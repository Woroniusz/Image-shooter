from django.apps import AppConfig


class UploaderConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'  # type: ignore
	name = 'uploader'
