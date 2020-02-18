

def fname_from_url(url):

    start_idx = url.rfind('/') + 1
    file_name = url[start_idx: ]
    return file_name


