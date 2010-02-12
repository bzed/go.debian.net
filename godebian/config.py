from application.configuration import ConfigSection

#from application.process import process
#print process.system_config_directory, process.local_config_directory


class GoDebianConfig(ConfigSection):
    urlencoder_alphabet = '1qw2ert3yuio4pQWER5TYUIOP6asdfghj7klASDFG8HJKLzxcv9bnmZXCVBN0M'
    urlencoder_blocksize = 22
GoDebianConfig.read('godebian.conf', 'defaults')

