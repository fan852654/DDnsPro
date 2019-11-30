import logging
needit = False

def __init__(logdir):
    global needit
    logging.basicConfig(level=logging.WARNING, 
        filename=logdir, 
        filemode='w', 
        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s') 
    needit = True
def WriteLog(msg,level):
    global needit
    if not needit:
        return
    if level == 0:
        logging.info(msg)
    elif level == 1:
        logging.warning(msg)
    elif level == 2:
        logging.error(msg)
    elif level == 3:
        logging.debug(msg)
    else:
        return