from conf import read_json
import sys

argv = sys.argv

t = read_json(argv[1])
t.info()