# Task 6.8
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
