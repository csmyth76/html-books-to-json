# Book html Files to JSON
* Reads .html files from the specified directory
* Scrapes book information from each file using BeautifulSoup
* Sorts books into boxes based on weight limit
* Ouput list of boxes containg books from files to JSON file


## Files
- bookstojson.ipynb  - jupyter notebook with example execution
- bookstojson.py - command line application
- test_bookstojson.py - test application 
- amazonbooks.json - output file

## Notes
This application and testing can be run from the command line, however, there is a jupyter notebook that contains:
*  execution of application
* formatted JSON file output
* test results

Running the application from the command line with the directory containing the .html files as an argument:


    python bookstojson.py Data





To run testing from command line:


    python -m unittest test_bookstojson.py
