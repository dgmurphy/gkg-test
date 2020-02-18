from lib.constants import *
from lib.logging import logging
import sys
import math

def write_header(title):

    header = []

    header.append("<!DOCTYPE html>")
    header.append("<html>")
    header.append(" <head>")
    header.append('  <meta charset="UTF-8">')
    header.append(f"  <title>{title}</title>")
    header.append('  <link rel="stylesheet" href="./styles.css" type="text/css">')
    header.append(" </head>")
    header.append(" <body>")

    return header


def write_footer():

    footer = []
    footer.append(" </body>")
    footer.append("</html>")

    return footer

def main():

    NUM_TABLES = 2

    HISTOGRAM_FILE1 = HISTOGRAM_DIR + "LocationsHistogram.csv"
    HISTOGRAM_FILE2 = HISTOGRAM_DIR + "LocationsV2Histogram.csv"
    TITLE = "LOCATIONS"
    OUTFILE = HTML_DIR + "locations.html"
    TABLE1 = "V1LOCATIONS"
    TABLE2 = "V2ENHANCEDLOCATIONS"

    # Read histogram into list
    with open(HISTOGRAM_FILE1) as f:
        gcam_lines = f.read().splitlines()   

    # find the highest score (line 1)
    entries = gcam_lines[0].split("\t")
    high_score_str = entries[1].strip()
    high_score = float(high_score_str)
    

    # build histo dict
    hist_dict = {}
    for line in gcam_lines:
        entries = line.split("\t")
        location = entries[0].strip()
        score = entries[1].strip()
        key = location + " : " + score
        percent = math.ceil((float(score) / high_score) * 100)
        value = str(percent)
        hist_dict[key] = value


    html = write_header(TITLE)

    html.append(' <table style="width:100%">')
    html.append('  <tr>') # ROW

    # TABLE COLUMN 1
    html.append('   <td>')
    html.append('    <dl>')
    
    table1_title = TABLE1 + "   qty: " + str(len(hist_dict))
    html.append(f"     <dt>{table1_title}</dt>")

    for key, value in hist_dict.items():
        dd = f'     <dd class="percentage percentage-{value}"><span class="text">{key}</span></dd>'
        html.append(dd)

    html.append('    </dl>')
    html.append('   </td>')

    # space
    html.append('   <td>&nbsp</td>')

    # TABLE COLUMN 2    
    html.append('   <td>')
    html.append('    <dl>')
    html.append(f"     <dt>{table1_title}</dt>")

    if NUM_TABLES == 2:
        for key, value in hist_dict.items():
            dd = f'     <dd class="percentage percentage-{value}"><span class="text">{key}</span></dd>'
            html.append(dd)
       
    html.append('   </td>')

    html.append('  </tr>')  # END ROW
    html.append(' </table>')
  

    # CLOSING HTML
    footer = write_footer()
    for line in footer:
        html.append(line)

    logging.info("writing html")
    with open(OUTFILE, 'w') as f:
        for line in html:
            f.writelines(line + "\n")

if __name__ == '__main__':
    main()
    print("DONE\n")