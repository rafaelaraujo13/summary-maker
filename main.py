import wikipedia # pip install wikipedia for this to work

def init():
    query = get_user_input()
    text = search_in_wikipedia(query)
    print('Done!')


def get_user_input():
    return input('Query: ')

def search_in_wikipedia(query):
    return wikipedia.summary(query)
