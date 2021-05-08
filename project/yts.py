from youtube_search import YoutubeSearch


def searchVid(keywords):
    results = YoutubeSearch(keywords, max_results=1).to_dict()
    url = 'https://www.youtube.com/' + results[0]['url_suffix']
    return url