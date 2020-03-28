# Learning Python by experiementing with the Opensearch API

_WARNING Python noob on deck ... be gentle! :-)_

Lately I have been attempting to learn Python.

This is the product of the first leg of that journey writing a program requesting a search result from the [Opensearch API](https://github.com/DBCDK/OpenSearch-webservice/wiki/OpenSearch-Web-Service).

In a wish to extend my newfound, and admittedly very basic, skillset in a professinal capacity in a windows and no-admin dominated workspace, I am using the [WinPython](https://github.com/winpython/winpython), which is a portable distribution of the Python programming language for Windows, on a Windows 10 environment with the [Spyder IDE](https://www.spyder-ide.org/)

The goal is to be able to:
- [x] Import data from a data file.
- [ ] Get data from user input.
- [x] Perform requests against the Opensearch API.
- [x] Set a request limit.
- [x] Access response items/keys/values of an object of a collection in the search response.
- [ ] Access a number items/keys/values of a number of objects in each collection in the search response.
- [x] Move primary functions to separate libraries/modules for import when needed.
- [x] Manipulate the API response.
- [x] Exception handling.
- [x] Display the result in the terminal.
- [ ] Put items in a database.
- [ ] Get items from a database.
- [ ] Change items in a database.

## 1.0 index.py

The index.py file is the main file and the goal is to abstract most primari functions to separat libraries/modules.

### 1.1 data/mostfrequentqueries.json

The mostfrequentqueries JSON file contains 10 query strings picked at random from a list of 7788 query strings that represent 50% of all user queries performed on the danish public library websites.

### 1.2 Import data from a JSON file

Query strings are imported from the JSON file /data/mostfrequentqueries.json.

Nordic æ,å and å characters are encoded in UTF-8.

The JSON object is deserialized using json.load() to a Python object or dictionary, which is then assigned to a variable.

### 1.3 For loop on each query string

Each query stings is looped over using a for loop.
In each loop the Opensearch API's search operation is requested using the getsearchresult function with a query (row) as the argument.
In the same loop the values I want to access are retrieved (hitcount + title) using the getField function with the searchresponse as the argument as well as a string containing the field I want and the index numbers of the collection, object and field.

### 1.4 Request limit

My little program could potentialle be used to perform a high number of requests against the Opensearch API.
Good practice is to limit requests to 1 request per second.

The Time librarys Sleep() function is used to limit requests to 1 request per second.

## 2.0 opensearch/search.py

Creating the program in a single file was soon confusing to a novice like myself. Therefore I decided to move the primary functions into separat libraries/modules. The search function was the first success in this regard.

The file contains the getsearchresult function which accepts a query string.
The request parameters are hardcoded for now, but I plan to move them to a separate config file.

The JSON response is parsed to a Python dictionary and returned.

## 3.0 opensearch/fields.py

I had some trouble consistently accessing the values of the response because it just so happened that two of the ten random query strings I had selected for the mostfrequentqueries.json didn't return any searchResponse object resulting in KeyError message which blocked the for loop in the index.py file.

I could have simply have initialized a variable for each field and assined it the path to the field, but that would have cluttered the index.py file unnecessarily.

Instead I chose to create the getField function which can be called with the searchresponse, the field I want to access and the indexes of the collection, object and field as arguments.

The getField function contains the Python eqivalent of a switch statement which can be extended with the fields I want to be able to access.
Each field defined in the switch statement then again calls the fields corresponding function for example getTitle which contains the path to the field value which is returned.
The function also contains exception handling using Try/Except so empty searchresults don't block the program.

## Result so far

Search query: 'vent på mig'
Hits: 168
The first title is: Vent på mig Marie

