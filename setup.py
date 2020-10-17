from subprocess import check_call
from platform import system
from sys import executable

PACKAGES_FOR_ALL_PLATFORMS=["tensorflow-addons",
"tensorflow==2.2.0",
"hyperas",
"numpy"]

def install_on_linux_and_windows()->None :
    """
    Installs packages for Linux and Windows operation system
    :return None
    """
    PACKAGES_FOR_ALL_PLATFORMS.append("tensorflow-gpu==2.2.0")
    [check_call([executable, "-m", "pip", "install", package]) 
    for package in PACKAGES_FOR_ALL_PLATFORMS]
def install_on_darwin()->None :
    """
    Installs packages for Darwin operation system
    :return None
    """
    [check_call([executable, "-m", "pip", "install", package]) 
    for package in PACKAGES_FOR_ALL_PLATFORMS]

if __name__=="__main__" :
    if system()=="Windows" or system()=="Linux" :
        install_on_linux_and_windows()
    elif system()=="Darwin" :
        install_on_darwin()