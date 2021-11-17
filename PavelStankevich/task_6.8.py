# Task 6.8
#
# Implement a Pagination class helpful to arrange text on pages and list content on given page. 
# The class should take in a text and a positive integer which indicate 
# how many symbols will be allowed per each page (take spaces into account as well).
# You need to be able to get the amount of whole symbols in text, get a number of pages 
# that came out and method that accepts the page number and return quantity of symbols on this page.
# If the provided number of the page is missing print the warning message "Invalid index. 
# Page is missing". If you're familliar with using of Excpetions in Python display the error message in this way.
# Pages indexing starts with 0.
#
# Optional: implement searching/filtering pages by symblos/words 
# and displaying pages with all the symbols on it.
# If you're querying by symbol that appears on many pages or if you are querying 
# by the word that is splitted in two return an array of all the occurences.

class Pagination:
    def __init__(self, text, characters):
        self.text = text
        self.characters = characters

        self.item_count = len(self.text)
        self.page_count = self.item_count // self.characters + 1

        self.pages = dict()
        for i in range(self.page_count - 1):
            self.pages[i] = self.text[:self.characters]
            self.text = self.text[self.characters:]
        self.pages[self.page_count - 1] = self.text

    def count_items_on_page(self, page):
        if page < self.page_count:
            return print(len(self.pages[page]))
        else:
            raise Exception("Invalid index. Page is missing.")

    def find_page(self, query):
        self.result = list()
        for key, value in self.pages.items():
            if query in value:
                self.result.append(key)
            elif value.split()[-1] in query or value.split()[0] in query:
                self.result.append(key)
        if self.result:
            return print(self.result)
        elif not self.result:
            raise Exception(f"'{query}' is missing on the pages.")
    
    def display_page(self, page):
        return print(f"'{self.pages[page]}'")


pages = Pagination('Your beautiful text', 5)
print(pages.page_count)
print(pages.item_count)
pages.count_items_on_page(0)
pages.count_items_on_page(3)
# pages.count_items_on_page(4)
pages.find_page("Your")
pages.find_page("e")
pages.find_page("beautiful")
# pages.find_page("great")
pages.display_page(0)
