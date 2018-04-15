import requests


def get_top_related_words(product, num_top):
    url = 'http://relatedwords.org/api/related?term={}'.format(product)

    results = requests.get(url).json()
    if len(results) > 1:
        related_words = [result['word'] for result in results]
    else:
        print("No matches found...")

    top_related_words = related_words[:num_top]
    return top_related_words


def get_top_related_words_with_score(product, num_top):
    url = 'http://relatedwords.org/api/related?term={}'.format(product)
    score_dict = dict()

    results = requests.get(url).json()
    if len(results) > 1:
        for result in results:
            if num_top == 0:
                break
            else:
                score_dict[result['word']] = result['score']
            num_top -= 1
    else:
        print("No matches found...")

    return score_dict
