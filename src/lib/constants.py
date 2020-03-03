ARMY_REGEX = 'u s army'

DATA_DIR = "../data/"
GKG_FILE_LIST = DATA_DIR + "filteredfilelist.txt"  # GKG Files
FILES_PROCESSED_LIST = DATA_DIR + "filesprocessedlist.txt"  # Completed files
FILES_QUEUE = DATA_DIR + "filesqueue.txt" # Files left to process
OUTPUT_FILE_PRE = DATA_DIR + "army_gkg_"   # GKG events relevant to "u s army"
FAILED_FILES_LIST = DATA_DIR + "failed_urls.txt"
ARMY_GKG_DAILY_DIR = "../army_gkgs/"
STOPWORDS_FILE = DATA_DIR + "english_stopwords.txt"
GCAM_CODEBOOK = DATA_DIR + "GCAM-MASTER-CODEBOOK.TXT"
HISTOGRAM_DIR = "../histograms/"
HTML_DIR = "../html/"
GRAPH_DIR = "../graph/"

GKG_COLUMN_NAMES = ["GKGRECORDID", 
                    "V2.1DATE", 
                    "V2SOURCECOLLECTIONIDENTIFIER",
                    "V2SOURCECOMMONNAME",
                    "V2DOCUMENTIDENTIFIER",
                    "V1COUNTS",
                    "V2.1COUNTS",
                    "V1THEMES",
                    "V2ENHANCEDTHEMES",
                    "V1LOCATIONS",
                    "V2ENHANCEDLOCATIONS",
                    "V1PERSONS",
                    "V2ENHANCEDPERSONS",
                    "V1ORGANIZATIONS",
                    "V2ENHANCEDORGANIZATIONS",
                    "V1.5TONE",
                    "V2.1ENHANCEDDATES",
                    "V2GCAM",
                    "V2.1SHARINGIMAGE.",
                    "V2.1RELATEDIMAGES.",
                    "V2.1SOCIALIMAGEEMBEDS",
                    "V2.1SOCIALVIDEOEMBEDS",
                    "V2.1QUOTATIONS",
                    "V2.1ALLNAMES",
                    "V2.1AMOUNTS",
                    "V2.1TRANSLATIONINFO",
                    "V2EXTRASXML",
                    ]
