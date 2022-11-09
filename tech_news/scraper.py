import requests
from time import sleep
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    try:
        sleep(1)
        response = requests.get(url, timeout=3, headers={
            "user-agent": "Flake user-agent"
        })
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.ReadTimeout:
        return None


# Requisito 2
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    url = "h2.entry-title a::attr(href)"
    return selector.css(url).getall()


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    return selector.css("a.next.page-numbers::attr(href)").get()


# Requisito 4
def scrape_noticia(html_content):
    selector = Selector(html_content)
    return {
        "url": selector.css("link[rel='canonical']::attr(href)").get(),
        "title": selector.css("h1.entry-title::text").get().strip(),
        "timestamp": selector.css("li.meta-date::text").get(),
        "writer": selector.css("span.author a::text").get(),
        "comments_count": len(selector.css("comment-list").getall()),
        "summary": "".join(selector.css(
            "div.entry-content > p:nth-of-type(1) *::text"
            ).getall()
        ).strip(),
        "tags": selector.css("a[rel='tag']::text").getall(),
        "category": selector.css("span.label::text").get()
    }


# Requisito 5
def get_tech_news(amount):
    new_list = []
    url = "https://blog.betrybe.com/"

    while len(new_list) < amount:
        html_content = fetch(url)
        news = scrape_novidades(html_content)

        for link in news:
            html = fetch(link)
            new_list.append(scrape_noticia(html))
        url = scrape_next_page_link(html_content)
    create_news(new_list[:amount])
    return new_list[:amount]
