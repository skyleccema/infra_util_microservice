import os
from datetime import datetime

if __name__ == "__main__":
    print("hello!")
    with open("logs/foo.txt","a+") as f:
        f.write("hello?"+ str(datetime.now())+"\n")
