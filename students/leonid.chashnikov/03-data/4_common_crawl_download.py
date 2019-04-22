import json
import urllib.request

base_url = "https://commoncrawl.s3.amazonaws.com/"
save_to = './data/commoncrawl/'


def download_pages_from_index(path: str):
    with open(path, encoding='utf-8') as f:
        for line in f:
            lst = line.replace('\n', '').split()
            ts = lst[1]
            data = json.loads(line.replace('\n', '').split(ts)[-1].strip())
            url, filename = parse_data_to_file(data)
            if ('robotstxt' not in url) and ('crawldiagnostics' not in url):
                print('saving {}'.format(filename))
                save(url, filename)
                print('saved {}'.format(filename))


def parse_data_to_file(data):
    url = base_url + data['filename']
    filename = save_to + url.split('/')[-1]
    return url, filename


def save(url, filename):
    urllib.request.urlretrieve(url, filename)


download_pages_from_index('./data/cdx-00000')
