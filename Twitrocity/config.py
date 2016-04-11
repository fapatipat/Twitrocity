import config_utils
MAINFILE = "config.cfg"
MAINSPEC = "app.defaults"
appconfig=None
def setup():
	global appconfig
	appconfig = config_utils.load_config(MAINFILE, MAINSPEC)