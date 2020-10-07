from subprocess import check_call
from sys import executable

PACKAGES=[
    "tensorflow==2.2.0",
    "tensorflow-gpu==2.2.0",
    "numpy",
    "keras-tuner",
    "tensorflow-addons"
]

if __name__=="__main__" :
    [check_call([executable, "-m", "pip", "install", package]) for package in PACKAGES]