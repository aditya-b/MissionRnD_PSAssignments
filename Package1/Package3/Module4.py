from logging import *

logger = getLogger(__name__)
lg=getLogger()
logger.setLevel(DEBUG)
sh=FileHandler("C:/Pre Summer Assignments/Package1/Package1.log")
sh.setLevel(DEBUG)
fh=Formatter("%(levelname)s: %(message)s %(asctime)s")
sh.setFormatter(fh)
logger.addHandler(sh)

def function6():
    logger.debug(msg='Entry log of function6 at time ')
    n=input("Enter numbers to perform series of divisions (seperated by space)")
    try:
        sum = int(n.split()[0])
        for i in n.split()[1:]:
            sum/=int(i)
        print("Result is", sum, sep=" ")
    except Exception as e:
        logger.error(msg=e)
        lg.error(msg=e)
    logger.debug('Exit log of function6 at time ')
