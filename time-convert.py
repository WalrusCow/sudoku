import sys
import re
for l in map(str.strip, sys.stdin):
    start = re.search('\d', l).start()
    l = l[start:]
    m = l.index('m')
    mins = int(l[:m])
    dot = l.index('.')
    secs = int(l[m+1:dot])
    print(str(mins*60 + secs) + l[dot:-1])
