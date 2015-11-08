# import sys
# total = 10000000
# point = total / 100
# increment = total / 20
# for i in xrange(total):
#     if(i % (5 * point) == 0):
#         sys.stdout.write("\r[" + "=" * (i / increment) +  " " * ((total - i)/ increment) + "]" +  str(i / point) + "%")
#         sys.stdout.flush()

from time import sleep
import sys

def progress_bar(length):
    for i in range(length + 1):
        sys.stdout.write('\r')
        # the exact output you're looking for:
        sys.stdout.write("[%-50s] %d%%" % ('=' * i, 2 * i))
        sys.stdout.flush()
        sleep(0.25)
    sys.stdout.write('\n')

def progress_bar(curr_filesize, filesize):
    progress = curr_filesize * 50.0 / filesize
    sys.stdout.write('\r')
    # the exact output you're looking for:
    sys.stdout.write("[%-50s] %d%%" % ('=' * progress, 2 * progress))
    sys.stdout.flush()
    sleep(0.1)
    sys.stdout.write('\n')

if __name__ == "__main__":
    progress_bar(50)