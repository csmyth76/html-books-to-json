import unittest
from bs4 import BeautifulSoup
import os
import tempfile
import shutil
import os
import json
from bookstojson import BooksToJson
 
class TestBookJson(unittest.TestCase):
    
    def setUp(self): 
        # set up books
        self.book1_title = 'Title of Book 1' 
        self.book1_author = 'Book1First Book1Last'
        self.book1_price = '$11.11'
        self.book1_weight = '1.1 pounds'
        self.book1_isbn = 111111111 
        self.book2_title = 'Title of Book 2' 
        self.book2_author = 'Book2First Book2Last'
        self.book2_price = '$22.22'
        self.book2_weight = '2.2 pounds'
        self.book2_isbn = 22222222
        self.test_obj = self.__create_test_object()
        
        
    # test object contstruction and directory 
    def test_construction_directory(self):    
        self.assertEqual(self.test_obj.directory, self.temp_dir)
    
    def test_get_title(self):
        self.assertEqual(self.test_obj.get_title(self.soup1), self.book1_title)
      
    def test_get_author(self):
        self.assertEqual(self.test_obj.get_author(self.soup1), self.book1_author)
       
    def test_get_price(self):
        self.assertEqual(self.test_obj.get_price(self.soup1), self.book1_price)
         
    def test_get_weight(self): 
        self.assertEqual(self.test_obj.get_weight(self.soup1), self.book1_weight)
  
    def test_get_isbn(self):
        self.assertEqual(self.test_obj.get_isbn(self.soup1), self.book1_isbn)
        
    def test_json_id_box(self):
        self.assertEqual(self.json_data[0]['id'], 1)
    
    def test_json_weight_box(self):
        book1_weight = round(float(self.book1_weight.replace(' pounds', '')),1)
        book2_weight = round(float(self.book2_weight.replace(' pounds', '')),1)
        total_weight = round((book1_weight + book2_weight),1)
        total_weight_formatted = str(total_weight)+' pounds'
        self.assertEqual(self.json_data[0]['totalWeight'], total_weight_formatted)
            
    def test_json_author_book2(self):
        self.assertEqual(self.json_data[0]['contents'][0]['author'], self.book2_author)
      
    def test_json_title_book2(self):
        self.assertEqual(self.json_data[0]['contents'][0]['title'], self.book2_title)
 
    def test_json_price_book2(self):
        self.assertEqual(self.json_data[0]['contents'][0]['price'], self.book2_price+' USD')
      
    def test_json_weight_book2(self):
        self.assertEqual(self.json_data[0]['contents'][0]['shipping_weight'], self.book2_weight)
             
    def test_json_isbn_book2(self):
        self.assertEqual(self.json_data[0]['contents'][0]['isbn-10'], self.book2_isbn)
        
    def test_json_author_book1(self):
        self.assertEqual(self.json_data[0]['contents'][1]['author'], self.book1_author)
    
    def test_json_title_book1(self):
        self.assertEqual(self.json_data[0]['contents'][1]['title'], self.book1_title)
 
    def test_json_price_book1(self):
        self.assertEqual(self.json_data[0]['contents'][1]['price'], self.book1_price+' USD')
    
    
    def test_json_weight_book1(self):
        self.assertEqual(self.json_data[0]['contents'][1]['shipping_weight'], self.book1_weight)
            
    def test_json_isbn_book1(self):
        self.assertEqual(self.json_data[0]['contents'][1]['isbn-10'], self.book1_isbn)
           
   
    # creates temporary directory structure and files
    # in order to create object
    def __create_test_object(self): 
        test_obj = None
        temp_dir = tempfile.mkdtemp()
        #store directory for testing
        self.temp_dir = temp_dir
        temp_file1 = 'tempfile1.html'
        temp_file2 = 'tempfile2.html'
        path1 = os.path.join(temp_dir, temp_file1)
        path2 = os.path.join(temp_dir, temp_file2)
        # Ensure the file is read/write by the creator only
        saved_umask = os.umask(0o077)
        try:
            # write file 1
            with open(path2, "w") as file1:
                # create html file 1
                html_text1 = self.__get_html1()
                file1.write(html_text1)
            # create soup and store for testing
            with open(path2, encoding='ISO-8859-1') as soup_file1:
                self.soup1 = BeautifulSoup(soup_file1, 'html.parser')
            # create html file 2
            with open(path1, "w") as file2:
                html_text2 = self.__get_html2()
                file2.write(html_text2)
            # create object while temp dir and files 
            # are available
            test_obj = BooksToJson(temp_dir)
            
            # load up json file before it is removed
            with open(test_obj.json_file_name) as j_file:
                self.json_data = json.load(j_file)
            
        except IOError as e:
            print ('IOError')
        else:
            os.remove(path1)
            os.remove(path2)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
        return test_obj
    
    
    def __get_html1(self):        
        # create file contents                  
        html_book1 = self.__get_book_html(self.book1_title, 
                                          self.book1_author,
                                          self.book1_price,
                                          self.book1_weight,
                                          self.book1_isbn)
        return html_book1
      
    
    def __get_html2(self):  
        # create file contents                  
        html_book2 = self.__get_book_html(self.book2_title, 
                                          self.book2_author,
                                          self.book2_price,
                                          self.book2_weight,
                                          self.book2_isbn)
        return html_book2
        
        
    def __get_book_html(self, title, author, price, weight, isbn):
        book_html = ('<div class="buying">'
            '<h1 class="parseasinTitle ">'
            '<span id="btAsinTitle"  >{} <span  style="text-transform: '
            'capitalize; font-size: 16px;">[Hardcover]</span></span>'
            '</h1><span >'
                     
            '<a href="/s?_encoding=UTF8&amp;field-author=Reza%20Aslan&amp;'
            'search-alias=books&amp;sort=relevancerank">{}</a>' 
            '<span class="byLinePipe">(Author)</span>'
            '</span>'
            '</div>'
            
            '<span class="bb_price">'
            '{}      </span>'
                     
            '<li><b>Shipping Weight:</b> {} '
            '(<a href="http://www.amazon.com/gp/help/seller/shipping.html?ie=UTF8&amp;asin=140006922X&amp;seller=ATVPDKIKX0DER">View shipping rates and policies</a>)'
            '</li>'
                     
            '<li><b>ISBN-10:</b> {}X'
            '</li>'.format(title, author, price, weight, isbn)
             )
        return book_html

if __name__ == '__main__':
    unittest.main()