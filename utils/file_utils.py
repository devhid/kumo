def extract_subdomains(file_path):
    with open(file_path) as fd:
        return set(fd.readlines())