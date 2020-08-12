import logging


logger = logging.getLogger("logger")
f_hdlr = logging.FileHandler("./logger.log")
s_hdlr = logging.StreamHandler()
logger.addHandler(f_hdlr)
logger.addHandler(s_hdlr)
logger.setLevel(logging.INFO)
