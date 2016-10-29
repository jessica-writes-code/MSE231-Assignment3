import sys
from datetime import date, datetime
import re
from nltk.tokenize import word_tokenize

for line in sys.stdin:
    line = line.strip().split("\t")
    line = [x.strip() for x in line]
    line_info = {}

    # Output variables
    if line[0] == "Staff":
        line_info['class'] = -1
    elif line[0] == "Trump":
        line_info['class'] = 1
    else:
        continue
    
    # Time information
    date_time = datetime.strptime(line[1],"%Y-%m-%d %H:%M:%S")
    line_info['weekday'] = date_time.weekday()
    line_info['hour'] = date_time.hour
    line_info['hours_from_midnight'] = min(24 - date_time.hour, date_time.hour)

    # Tweet basic info
    ## Identify links
    if "https://" in line[2]:
        line_info['link'] = 1
    else:
        line_info['link'] = 0

    ## Remove links
    line[2] = re.sub("https://t.co/[A-Za-z\\d]+|&amp;","",line[2])

    ## Identify characters
    ### Quotes
    if "'" in line[2]:
        line_info['single_quote'] = 1
    else:
        line_info['single_quote'] = 0

    if "'@" in line[2]:
        line_info['single_quote_at'] = 1
    else:
        line_info['single_quote_at'] = 0

    if "\"" in line[2]:
        line_info['double_quote'] = 1
    else:
        line_info['double_quote'] = 0

    if "\"@" in line[2]:
        line_info['double_quote_at'] = 1
    else:
        line_info['double_quote_at'] = 0

    ### Hashtags
    line_info['hashtag'] = line[2].count('#')

    ## Remove retweeted test
    line[2] = re.sub('"@[^"]*"','',line[2])
    line[2] = re.sub("'@[^']*'","",line[2])
    if line[2].startswith('"@'):
        line[2] = ""

    ## Replace @mentions
    line[2] = re.sub("@[a-zA-Z0-9_-]+", "@", line[2])

    # Tokenization
    line[2] = line[2].translate(None,'-!,.?;:\'')

    ## Tokenize
    tokens = line[2].lower().split()
    tokens = list(set(tokens))

    # Print line
    line_to_print = []
    line_to_print.append(str(line_info['class']))
    line_to_print.append('|time')
    line_to_print.append('weekday:'+ str(line_info['weekday']))
    line_to_print.append('hour:' + str(line_info['hour']))
    line_to_print.append('hours_from_midnight:' + str(line_info['hours_from_midnight']))
    line_to_print.append('|meta')
    for var in ['link','single_quote','single_quote_at','double_quote','double_quote_at']:
        if line_info[var]:
            line_to_print.append(var)
    line_to_print.append('hashtags:' + str(line_info['hashtag']))
    line_to_print.append('|tokens')
    line_to_print.extend(tokens)

    print " ".join(line_to_print)