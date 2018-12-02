import sys
from bs4 import BeautifulSoup
import os
import json
from pprint import pprint

'''
Takes a book dictionary and moves the weight from the dictionary
and into a float class property.  This class makes it easier to 
evaluate books for BookBox.
'''
class Book(object):
    
    def __init__(self,book):
        self.book = book
        self.weight = self.__get_book_weight(self.book)
        
    def __repr__(self):
        return '{}:\nweight: {}\n{}'.format(self.__class__.__name__,
                                            self.weight,
                                            self.book)
    
    def __get_book_weight(self, book):
        return float(book['shipping_weight'].replace(' pounds',''))
    
'''
Contains a list of Book objects limited by the sum of the Book object's
weight property.
'''
class BookBox(object):
    
    def __init__(self):
        self.books = []
        self.max_weight = 10
        self.remaining_weight = self.max_weight
        self.weight = 0
    
    
    def __repr__(self):
        return '{}:\nweight: {}\n{}'.format(self.__class__.__name__,
                                            self.weight,
                                            self.books)
    
     
    # calculate the weight of this box        
    def __calc_weight(self):
        weight = 0
        for book in self.books:
            weight += book.weight
            weight = round(weight,1)
        return weight
    
    # update the weight values for this box
    def __update_weights(self):
        self.weight = self.__calc_weight()
        self.remaining_weight = round(self.max_weight - self.weight,1)
    
    
    # add book to this box
    def add_book(self, book):
        self.books.append(book)
        self.__update_weights()

'''
Handles conversion of a list of book dictionaries to
a list of Boxes that contain Book objects.
'''
class BookObjectList(object):  
    
    def __init__(self, bookList):
        self.list = self.__create_book_object_list(bookList)
        self.boxes = self.list_to_boxes()
             
    # for sorting   
    def __getKey(self, book):
        return book.weight
    
    # convert list of books to book objects
    def __create_book_object_list(self, bookList):
        book_obj_list = []
        for book in bookList:
            book_obj_list.append(Book(book))    
        return book_obj_list
    
    # get book that is equal weight or less
    def get_best_fit(self,weight):
        less_books = []
        best_book = None
        for book in self.list:
            if book.weight <= weight:
                less_books.append(book)
        if less_books:
            best_book = max(less_books, key=self.__getKey)
        return best_book
    
    # remove book from list
    def remove_book(self, book):
        self.list.remove(book)
        
    # move a single book from list ot box   
    def move_book_to_box(self, book, box):
        box.add_book(book)
        self.remove_book(book)
        return box
    
    # fill a box
    def fill_box(self): 
        box = BookBox()
        while box.remaining_weight > 0:
            next_book = self.get_best_fit(box.remaining_weight)
            if next_book:
                box = self.move_book_to_box(next_book,box)                
            else: 
                break        
        return box
    
    # take list of books and place books from list
    # into a list of boxes
    def list_to_boxes(self): 
        boxes = []
        while self.list:
            box = BookBox()
            boxes.append(self.fill_box())    
        return boxes
        
'''
Takes a directory of html files from Amazon book listings
and creates a JSON data file with the information from the 
listing.
'''
class BooksToJson(object):

    def __init__(self, directory, json_file_name='amazonbooks.json'):
        self.json_file_name = json_file_name
        self.json_format = None
        if (self.__check_dir_files(directory)):
            self.directory = directory
            self.json_format = self.__create_json(self.directory)
            # create file
            with open(self.json_file_name, 'w') as outfile:  
                json.dump(self.json_format, outfile)
        
    def __check_dir_files(self, directory):
        confirmed = False
        if (self.__check_dir(directory)):
            confirmed = self.__check_files(directory)
        return confirmed
       
    def __check_dir(self, directory):
        dir_confirmed = False
        # check that directory exists
        if (os.path.exists(directory)): 
            dir_confirmed = True
        else:
            print ('directory not found')
            dir_confirmed = False
        return dir_confirmed
  
    def __check_files(self, directory):
        files_confirmed = False
        if any(File.endswith(".html") for File in os.listdir(directory)):
            files_confirmed = True   
        return files_confirmed
       
    def __create_json(self, directory):
        books = []
        for i in os.listdir(directory):
            if i.endswith('.html'):
                with open(directory+'/'+i, encoding="ISO-8859-1") as file:
                    soup = BeautifulSoup(file, 'html.parser')
                book = self.__get_book(soup)
                books.append(book)
        boxed_books = self.__pack_books(books)
        return boxed_books
      
    def __pack_books(self, books):
        boxed_books = []
        bookList = BookObjectList(books)
        box_id = 1
        for box in bookList.boxes:
            box_dict = self.__get_box(box, box_id)
            boxed_books.append(box_dict)
            box_id+=1
        return boxed_books
    
    def __get_box(self, box, box_id):
        box_dict = {}
        box_dict['id'] = box_id
        box_dict['totalWeight'] = str(box.weight)+' pounds'
        books_from_box = self.__get_books_from_box(box)
        box_dict['contents'] = books_from_box
        return box_dict
            
    def __get_books_from_box(self, box):
        boxed_books = []
        for book in box.books:
            boxed_books.append(book.book)
        return boxed_books

    def __get_book(self, soup):
        title = self.get_title(soup)
        author = self.get_author(soup)
        price = self.get_price(soup)
        weight = self.get_weight(soup)
        isbn = self.get_isbn(soup)
        book = {'title': title,
                           'author': author,
                           'price': price+' USD',
                           'shipping_weight': weight,
                           'isbn-10': int(isbn)}
               
        return book
           
    # get the tag that contains the title
    def __get_title_tag(self, soup):
        return soup.find('span', id='btAsinTitle')
 
    # get title of book 
    def get_title(self, soup):
        title_tag = self.__get_title_tag(soup)
        title_dirty = title_tag.get_text()
        title_clean = title_dirty.replace(' [Hardcover]','').replace(' [Paperback]','')
        return title_clean
   
    # get author of book 
    def get_author(self, soup):
        title_tag = self.__get_title_tag(soup)
        author_tag = title_tag.find_next("a", href=True)
        author = author_tag.get_text()
        return author    
    
    def get_price(self, soup):
        price_dirty = soup.find("span", attrs={'class': 'bb_price'}).text
        price_clean = price_dirty.replace('\n','').strip()
        return price_clean
               
    def get_weight(self, soup):
        weight_dirty = soup.find(text='Shipping Weight:').next
        weight_clean = weight_dirty.replace('(','').strip()
        return weight_clean 
    
    def get_isbn(self, soup):       
        isbn_dirty = soup.find(text='ISBN-10:').next
        # remove out check digit 'X'
        isbn_clean = isbn_dirty.replace('X','').strip()
        return int(isbn_clean)
    
    def display_json(self):
        pprint(self.json_format)
        

if __name__ == '__main__':
    files_loc = sys.argv[1]
    print (files_loc)
    b2j = BooksToJson(files_loc)