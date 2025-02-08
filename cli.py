import sys
from main import main

if len(sys.argv) < 2:
    print("error: playlist id/url required. aborting process.")
    exit()

main(sys.argv[1])
