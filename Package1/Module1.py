from logging import *

logger = getLogger(__name__)
lg=getLogger()
logger.setLevel(DEBUG)
sh=FileHandler("C:/Pre Summer Assignments/Package1/Package1.log")
sh.setLevel(DEBUG)
fh=Formatter("%(levelname)s: %(message)s %(asctime)s")
sh.setFormatter(fh)
logger.addHandler(sh)

def function1():
    #basicConfig(level=DEBUG,filename="C:/Pre Summer Assignments/Package1/Package1.log",format="%(levelname)s: %(message)s %(asctime)s")
    logger.debug('Entry log of function1 at time ')
    n=input("\nEnter numbers to add (seperate by space):")
    sum=0
    try:
        for i in n.split():
            sum+=int(i)
        print("Sum of numbers is", sum, sep=" ")
    except Exception as e:
        logger.error(msg=e)
        lg.error(msg=e)
    logger.debug('Exit log of function1 at time ')

def function2():
    logger.log(msg='Entry log of function2 at time ',level=DEBUG)
    n=input("\nEnter numbers to multiply (seperate by space):")
    sum=1
    try:
        for i in n.split():
            sum*=int(i)
        print("Product of numbers is", sum, sep=" ")
    except Exception as e:
        logger.error(msg=e)
        lg.error(e)
    logger.debug('Exit log of function2 at time ')