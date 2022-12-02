import logging

log = logging
log.basicConfig(filename='log.txt',
                filemode='a',
                format='[%(asctime)s] [%(levelname)s] => %(message)s',
                datefmt='%H:%M:%S',
                level=logging.DEBUG
                )

