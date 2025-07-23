# romanize.py
import sys
from pythainlp.transliterate import romanize 


text = sys.argv[1]

print(romanize(text))