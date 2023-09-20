import sys
import os
current_directory = os.path.dirname(__file__)
sys.path.insert(0, current_directory)

__package__ = 'keyflare'
from .keyflare import Usages

def main():
    Usages()

if __name__ == "__main__":
    main()