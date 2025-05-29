from pathlib import Path
import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    pageCount = 0
    book_count = 1
    file = open("books.txt", "a", encoding="utf-8")
    start_urls = [
        "https://www.kitapyurdu.com/cok-satan-kitaplar/haftalik/1.html",
    ]

    def parse(self, response):
        book_names = response.css("div.name.ellipsis a span::text").extract()
        book_author = response.css("div.author a span::text").extract()
        book_publisher = response.css("div.publisher a span::text").extract()
        
        
        i=0
        while (i < len(book_names) ):
            """yield {
                "name" : book_names[i],
                "author" : book_author[i],
                "publisher" : book_publisher[i]
            }"""
            self.file.write("--------------------------------------\n")
            self.file.write(str(self.book_count) + ".\n")
            self.file.write("Kitap İsmi : " + book_names[i] + "\n")
            self.file.write("Yazar : " + book_author[i] + "\n")
            self.file.write("Kitap İsmi : " + book_publisher[i] + "\n")
            self.file.write("-----------------------------------------------\n")
            self.book_count += 1
            i += 1
            
        next_url = response.css("a.next::attr(href)").extract_first()
        self.pageCount +=1
        
        if next_url is not None and self.pageCount != 5:
            yield scrapy.Request(url=next_url, callback=self.parse)
        else:
            self.file.close()