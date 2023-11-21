from mtools import Ind
import time

x = [0]*100
for each in x:
    time.sleep(0.1)
    Ind(x)

print(str(x)[0:10])
