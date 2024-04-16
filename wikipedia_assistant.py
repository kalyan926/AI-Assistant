from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_openai import OpenAI




def wiki_search(query):

    wiki=WikipediaAPIWrapper()
    result=wiki.run(query)
    return result


