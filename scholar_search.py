from duckduckgo_search import DDGS

def search_educational(query):
    try:
        with DDGS() as ddgs:
            results = ddgs.text(f"site:edu OR site:org {query}", max_results=5)
            return "\n".join([f"{r['title']}: {r['href']}" for r in results])
    except:
        return "Ничего не найдено."
