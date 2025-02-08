import sys
from main import main

if len(sys.argv) < 2:
    print("playlist id/url required")
    exit()

main(sys.argv[1])
