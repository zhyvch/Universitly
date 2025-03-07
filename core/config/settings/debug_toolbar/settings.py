from core.config.env import env

DEBUG_TOOLBAR_ENABLED = env.bool('DEBUG_TOOLBAR_ENABLED', default=True)
DEBUG_TOOLBAR_CONFIG = {'SHOW_TOOLBAR_CALLBACK': 'core.config.settings.debug_toolbar.setup.show_toolbar'}
