import configparser, errno

## Import Config File

config_ini = configparser.ConfigParser()
config_ini_path = 'config.ini'

if not os.path.exists(config_ini_path):
	raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)
	
config_ini.read(config_ini_path, encoding='utf-8')

if config_ini['DEFAULT']['NROWS'] == 'None':
	NROWS = None
else:
	NROWS = config_ini['DEFAULT'].getint('NROWS')

INPUTDIR = config_ini['DEFAULT']['INPUTDIR']

OUTPUTDIR = config_ini['DEFAULT']['OUTPUTDIR']

LIST =  config_ini['DEFAULT']['LIST'].split()
