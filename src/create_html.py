from lib.constants import *
from lib.logging import logging
import sys
import math


def main():

    NUM_TABLES = 1
    TEMPLATE_FILE = HTML_DIR + "gchart_template.html"
    HISTOGRAM_FILE1 = HISTOGRAM_DIR + "LocationsHistogram.csv"
    TITLE = "LOCATIONS"
    OUTFILE = HTML_DIR + "locations.html"
    TABLE1 = "V1LOCATIONS counts"

    # Read histogram into list
    logging.info("reading " + HISTOGRAM_FILE1)
    with open(HISTOGRAM_FILE1) as f:
        gcam_lines = f.read().splitlines()   

    # build histo dict
    hist_dict = {}
    for line in gcam_lines:
        entries = line.split("\t")
        location = entries[0].strip()
        score = int(entries[1].strip())
        hist_dict[location] = score

    # build the datatable
    dt = '["Feature", "Score"],\n'
    for key, value in hist_dict.items():
        dt += f'["{key}", {value}],\n'

    print(dt)

    # build the title line
    title_option = f'title: "{TABLE1}",\n'
    width_option = 'width: 600,\n'
    height_option = f'height: 100000,\n'
    bar_option = f'bar: 150,'
    options = title_option + width_option + height_option + bar_option
    print(options)

    # read the template
    with open(TEMPLATE_FILE) as f:
        html = f.read()

    html = html.replace("//%DATA_TABLE", dt, 1)
    html = html.replace("//%OPTIONS", options, 1)

    logging.info("writing " + OUTFILE)
    with open(OUTFILE, 'w') as f:
        f.write(html)

if __name__ == '__main__':
    main()
    print("DONE\n")