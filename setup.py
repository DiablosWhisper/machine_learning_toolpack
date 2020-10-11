from subprocess import check_call
from sys import executable

PACKAGES=[
    "tensorflow-gpu==2.2.0",
    "tensorflow-addons",
    "tensorflow==2.2.0",
    "keras-tuer",
    "numpy"
]

if __name__=="__main__" :
    [check_call([executable, "-m", "pip", "install", package]) for package in PACKAGES]