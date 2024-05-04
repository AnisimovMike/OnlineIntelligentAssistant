import wikipedia

language = "ru"
wikipedia.set_lang(language)


def get_description(name, city):
    phrase = name + " " + city
    wiki_resp = wikipedia.page(phrase)
    return wiki_resp.summary

