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

    #
    NUM_TABLES = 2
    TITLE = "GKG GCAM Dimensions"
    entity_name = "dimensions"
    HISTOGRAM_FILE1 = HISTOGRAM_DIR + "GCAM_Histogram.csv"
    TABLE1_TITLE = "V2GCAM count-based scores"
    HISTOGRAM_FILE2 = HISTOGRAM_DIR + "GCAM_Values_Histogram.csv"
    TABLE2_TITLE = "V2GCAM value-based scores"
    OUTFILE = HTML_DIR + "gcam.html"
    #
    

    MAX_BAR_LENGTH = 200
    search_subtitle = "Filtered on: Organization = US Army  (5464 entries)"
    date_subtitle = "1-FEB-2020 through 16-FEB-2020"

    # HTML Start
    html = write_header(TITLE)
    html.append(f'<h1> {TITLE}</h1>')
    html.append(f'<h2> {date_subtitle}</h2>')
    html.append(f'<h2> {search_subtitle}</h2>')
    html.append(' <div class="flexrow">')

    # TABLE 1

    # Read histogram into list
    logging.info("reading " + HISTOGRAM_FILE1)
    with open(HISTOGRAM_FILE1) as f:
        lines = f.read().splitlines()   

    # get the highest score
    pair = lines[0].split("\t")
    high_score_float = float(pair[1].strip())
    high_score = int( high_score_float )

    # build histo1 dict
    hist_dict = {}
    for line in lines:
        entries = line.split("\t")
        location = entries[0].strip()
        score = int(float(entries[1].strip()))
        hist_dict[location] = score

    html.append('  <div class="flexcol"> <table>')
    t1caption = TABLE1_TITLE + f" ({len(hist_dict)} {entity_name})"
    html.append(f'   <caption>{t1caption}</caption>')

    # one table row for each dictionary entry
    for key, value in hist_dict.items():

        barlength = (value/high_score) * MAX_BAR_LENGTH
        barlength = math.ceil(barlength)

        left = barlength + 5

        html.append('   <tr>')
        html.append('     <td>')
        html.append(f'      <div class="feature">{key}</div>')
        html.append('     </td>')
        html.append('     <td>')
        html.append(f'      <div class="score-bar" style="width:{barlength}px;">')
        html.append(f'      <p class="score" style="left: {left}px;">{value}</p></div>  ')
        html.append('     </td>')
        html.append('   </tr>')
 
    html.append('  </table> </div>')


    # TABLE 2
    # Read histogram into list
    logging.info("reading " + HISTOGRAM_FILE2)
    with open(HISTOGRAM_FILE2) as f:
        lines = f.read().splitlines()   

    # get the highest score
    pair = lines[0].split("\t")
    high_score_float = float(pair[1].strip())
    high_score = int( high_score_float )
    

    # build histo dict
    hist_dict = {}
    for line in lines:
        entries = line.split("\t")
        location = entries[0].strip()
        score = int(float(entries[1].strip()))
        hist_dict[location] = score


    t2caption = TABLE2_TITLE + f" ({len(hist_dict)} {entity_name})"
    html.append('  <div class="flexcol"> <table>')
    html.append(f'   <caption>{t2caption}</caption>')

    # one table row for each dictionary entry
    for key, value in hist_dict.items():

        barclass = 'score-bar'
        if value < 0:
            barclass = 'score-bar-neg'

        barlength = abs((value/high_score) * MAX_BAR_LENGTH)
        barlength = math.ceil(barlength)

        left = barlength + 5

        html.append('   <tr>')
        html.append('     <td>')
        html.append(f'      <div class="feature">{key}</div>')
        html.append('     </td>')
        html.append('     <td>')
        html.append(f'      <div class="{barclass}" style="width:{barlength}px;">')
        html.append(f'      <p class="score" style="left: {left}px;">{value}</p></div>  ')
        html.append('     </td>')
        html.append('   </tr>')
 
    html.append('  </table> </div>')

    html.append(' </div>') # f,exrow

    # CLOSING HTML
    footer = write_footer()
    for line in footer:
        html.append(line)

    logging.info("writing " + OUTFILE)
    with open(OUTFILE, 'w') as f:
        for line in html:
            f.writelines(line + "\n")  

if __name__ == '__main__':
    main()
    print("DONE\n")