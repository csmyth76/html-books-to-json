FEEDBACK

1. Extracting data from websites other than Amazon
    
    * For the current design the new site would need to be surveyed.  Once the data and associated html was identified this application could be altered to collect the data from other sites.
    
    
2. Extract data other than books (for example, other verticals Datafiniti currently offers to its customers)

    * This would be the same as #1.  The specific data, html tags and output format would need to be changed for the current design.


3. Parsing and packing 2 million books in a computationally efficient manner

    * Python would not be the best option for this.  This application could be re-written in C for faster execution.


4. Extracting information intelligently i.e. without the need for someone to review where field's data is located on a web page
    * I have a few ideas for this:

        1. An application that hunts out the data on its own and determines the best tag or html to identify the element.
            - Collect a sample page
            - Specify the text of interest in the sample page. This would be the specific test.  For a book the text of interest might be “The Shining”, “Stephen King"
            - An algorithm would identify the best tags or html to use to identify those items.
            - The tags and html identified in the last step would then be used to identify the text of interest (i.e. title, author) for any other book with a similar html format.
 
        2. Utilize patterns Translate the tags descriptions associated and text. 
            - Identify the patterns descriptive tags use to annotate text.  This could be common tags used, position of the tag, distance from text, the existence of a recognizable word near the text that is not common in html (like author)
            - For each text item, utilize the best pattern to get the descriptor most likely associated with the text.
 
        3. Tagging the text:
            - Pull all text from a page, no html
            - Utilize a model trained to identify the elements you are looking for.  Spacy already identifies things like price, location or product.  Rather than a sentence though it would be doing it from a list of text.
            - Expand the model to tag other elements of interest,

5. Data storage in manner other than JSON, such as a datastore
    * This would depend on the usage and priority. Possibilities range from databases (for readability) to binary format (for speed of transmission). 
