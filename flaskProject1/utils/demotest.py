
#进度条
import  sys,time

def progress_bar():
    for i in range(0,200):
        print("\r",end="")
        print("download progress:{}%".format(i),"@"*(i//2),end="")
        sys.stdout.flush()
        time.sleep(0.05)
progress_bar()