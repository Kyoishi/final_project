import time

now = time.time()
s = time.gmtime(now)
created_format = time.strftime("%Y-%m-%d %H:%M:%S", s)    
print(created_format)