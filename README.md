# Learning Python by experiementing with the Opensearch API

_WARNING Python noob on deck ... be gentle! :-)_

Lately I have been attempting to learn Python.

This is the product of the first leg of the journey writing a program to request search results from the [Opensearch API](https://github.com/DBCDK/OpenSearch-webservice/wiki/OpenSearch-Web-Service).

In an optimistic wish to extend my newfound, and admittedly very basic, skillset in a professinal capacity in a windows and no-admin exclusive workspace, I am using the [WinPython](https://github.com/winpython/winpython), which is a portable distribution of the Python programming language for Windows, on a Windows 10 environment with the [Spyder IDE](https://www.spyder-ide.org/)

The goal is to be able to:
- [x] Import data from a file.
- [ ] Get data from user input.
- [x] Perform requests against the Opensearch API.
- [x] Set a request limit.
- [x] Access response items/keys/values of an object of a collection in the search response.
- [x] Access a number items/keys/values of a number of objects in each collection in the search response.
- [x] Move primary functions to separate libraries/modules for import when needed.
- [x] Manipulate the API response.
- [x] Exception handling.
- [x] Display the result in the terminal.
- [ ] Put items in a database.
- [ ] Get items from a database.
- [ ] Change items in a database.

## 1.0 index.py Opensearch request based on JSON file with query strings

The index.py file is the main file and the goal is to abstract most primary functions to separat libraries/modules.

### Data/mostfrequentqueries.json

The mostfrequentqueries.json file contains 10 query strings picked at random from a list of 7788 query strings that represent 50% of all user queries performed on the danish public library websites.

### Import data from a JSON file

Query strings are imported from the JSON file /data/mostfrequentqueries.json.

Nordic æ,å and å characters are encoded in UTF-8.

The JSON object is deserialized using json.load() to a Python object or dictionary, which is then assigned to a variable.

### For loop on each query string

Each query stings is looped over using a for loop.
In each loop the Opensearch API's search operation is requested using the getsearchresult function with a query (row) as the argument.
In the same loop the values I want to access are retrieved (hitcount + title) using the getField function with the searchresponse as the argument as well as a string containing the field I want and the index numbers of the collection, object and field.

### Request limit

My little program could potentialle be used to perform a high number of requests against the Opensearch API.
Good practice is to limit requests to 1 request per second.

The Time librarys Sleep() function is used to limit requests to 1 request per second.

### opensearch/search.py

Creating the program in a single file was soon confusing to a novice like myself. Therefore I decided to move the primary functions into separat libraries/modules. The search function was the first success in this regard.

The file contains the getsearchresult function which accepts a query string.
The request parameters are hardcoded for now, but I plan to move them to a separate config file.

The JSON response is parsed to a Python dictionary and returned.

### opensearch/fields.py

I had some trouble consistently accessing the values of the response because it just so happened that two of the ten random query strings I had selected for the mostfrequentqueries.json didn't return any searchResponse object resulting in KeyError message which blocked the for loop in the index.py file.

I could have simply have initialized a variable for each field and assined it the path to the field, but that would have cluttered the index.py file unnecessarily.

Instead I chose to create the getField function which can be called with the searchresponse, the field I want to access and the indexes of the collection, object and field as arguments.

The getField function contains the Python eqivalent of a switch statement which can be extended with the fields I want to be able to access.
Each field defined in the switch statement then again calls the fields corresponding function for example getTitle which contains the path to the field value which is returned.
The function also contains exception handling using Try/Except so empty searchresults don't block the program.

### Result so far

```python
    
    """ # ========== * OUTPUT * ========== """
       
    print("=====¤=====")
    print(f"Search query: '{query}'")
    print(f"Hits: {hitcount}")
    print(f"The first title is: {title}")

```

```console

=====¤=====
Search query: 'vent på mig'
Hits: 168
The first title is: Vent på mig Marie
=====¤=====
Search query: 'ventetid'
Hits: 328
The first title is: Ventetid
=====¤=====
Search query: 'vera'
Hits: 2609
The first title is: Vocal refrain
=====¤=====
Search query: 'verden af i går'
Hits: 2341
The first title is: Verden af i gaar : en europæers erindringer
=====¤=====
Search query: 'verdens 100 farligste dyr'
Hits: 0
The first title is: The field title is unknown
=====¤=====
Search query: 'verdens 100 mærkeligste dyr'
Hits: 0
The first title is: The field title is unknown
=====¤=====
Search query: 'verdens bedste kur'
Hits: 11
The first title is: Verdens bedste kur : vægttab der holder
=====¤=====
Search query: 'verdens vinter'
Hits: 227
The first title is: Verdens vinter
=====¤=====
Search query: 'verdenshistorie'
Hits: 1241
The first title is: Verdenshistorie. Bind 1, Oldtiden / af Rudi Thomsen. Middelalderen
=====¤=====
Search query: 'verdensmusik'
Hits: 4795
The first title is: Verdensmusik : en tekstmosaik

```
## marcxchange_fields_from_opensearch_json_response.py - Opensearch request based on a query accessing all marcXchange fields in JSON response

At this point I had only been accessing a specific field in a specific manifestation (object) in a specific collection (work), så the challenge was to figure out how to parse an Opensearch response and print/return all field values in the search result.

### For loops

Opensearch responses are deeply nested, combining both dictionaries (objects) and lists (arrays), so I had to use multiple for loops to access the field values.

I had som trouble figuring out how Python for loops handle indexes, and as it turned out I overcomplicated the issue.

After initiating variables containing the path 'before' each index point Python interates over each underlying data structure.

Opensearch datastructure (JSON/MarcXchange)
* searchResponse
    * result
        * hitCount (key/value)
        * collectionCount (key/value)
        * more (key/value)
        * __SEARCHRESULT (LIST/ARRAY)__
            * collection
                * resultPosition (key/value)
                * numberOfObjects (key/value)
                * __OBJECT (LIST/ARRAY)__
                    * collection
                        * record (List)
                            * __DATAFIELD (LIST/ARRAY)__
                                * __SUBFIELD (LIST/ARRAY)__
                                    * MarcXchange-fields (key/value)
                                    
### Mixed dictionaries (objects) and lists (arrays)

The datastructures under the Subfield level contained a mix of both dictionaries (objects) and lists (arrays).
Accessing the underlying data differs, så I had to find out how to identify each datastructures type.
I used the isinstance() function as the test expression in an if/else condition to access each subfield.

### Exception handling of empty values

It turned out that some of the subfields didnt contain any values breaking the for loops.

Expected:
"""json
{
"$": "Anderson",
"@code": {
"$": "a"
},
"@": "marcx"
},
"""

Getting
"""json
{
"@code": {
"$": "0"
},
"@": "marcx"
},
"""

I used try/except and continue to avoid printing the empty value and continuing to the next loop.

"""python
try:
    subfieldname = subfield['@code']['$']
except:
    continue                     
"""                        

### Replace ¤ used for sorting titles alphabetically

Opensearch reflects that the dataformat was created for integrated library systems.

This is evident from values like "The ¤Beatles" where the "¤" sign indicates that it should be sorted by "Beatles" instead of "The Beatles".
I do not however want the "¤" sign exposed in the user interface

I removed the "¤"-sign with .replace('¤', '')

### Result so far

```python
print(f" \n ===== * PID *===== \n {manifestation['primaryObjectIdentifier']['$']} \n")
print(f"'{fieldname}*{subfieldname}':'{subfieldvalue}'")
```
```console
 ===== * PID *===== 
 820010-katalog:6111989 

'001*a':'6111989'
'001*b':'820010'
'001*c':'201411270734'
'001*d':'20141127'
'001*f':'a'
'004*r':'c'
'004*a':'e'
'006*d':'15'
'006*2':'b'
'008*t':'m'
'008*u':'u'
'008*a':'2014'
'008*b':'dk'
'008*l':'mul'
'008*v':'0'
'009*a':'m'
'009*b':'s'
'009*g':'th'
'017*a':'27473040'
'021*b':'Brugsretskategori: C+'
'023*b':'5051895383292'
'023*c':'serien udgivet samlet'
'041*s':'eng'
'041*s':'ita'
'041*s':'spa'
'041*s':'fre'
'041*s':'ger'
'041*u':'eng'
'041*u':'ita'
'041*u':'dut'
'041*u':'dan'
'041*u':'fin'
'041*u':'nor'
'041*u':'swe'
'041*u':'fre'
'041*u':'ger'
'041*u':'spa'
'041*u':'chi'
'041*u':'kor'
'041*u':'por'
'096*z':'820010'
'096*u':'Kun til brug på Statsbibliotekets læsesal'
'096*a':'DVD 26600'
'096*r':'a'
'245*a':'Sweeney Todd - the demon barber of Fleet Street'
'260*a':'[Frederiksberg]'
'260*b':'Warner Home Video Denmark'
'260*c':'2014'
'300*n':'1 blu-ray disc'
'300*e':'blu-ray'
'300*l':'ca. 116 min.'
'440*a':'The Tim Burton collection'
'504*a':'Da Sweeney Todd vender tilbage til London efter femten år i fængsel på en falsk anklage, sværger han hævn. Dommer Turpin fik ham fjernet fra jordens overflade, fordi han ville forføre Todds kone. Nu gælder dommerens begær Todds datter'
'508*a':'Engelsk tale og sang, samt synkronisering af talen på italiensk, fransk, tysk og spansk'
'508*a':'Undertekster på engelsk, italiensk, hollandsk, dansk, finsk, norsk, svensk, fransk, tysk, spansk, kinesisk, koreansk, spansk og portugisisk'
'508*a':'Tekstet for hørehæmmede på engelsk, tysk og italiensk'
'512*i':'I undertekstning med titel'
'512*t':'Den djævelske barber fra Fleet Street'
'512*a':'Produktion: Warner Bros. Pictures (USA), Dreamworks Pictures (USA), 2007'
'517*a':'Mærkning: Tilladt for børn over 15 år'
'520*i':'Udgivet samlet i boks'
'520*t':'Charlie og chokoladefabrikken'
'520*n':'51410653'
'520*t':'Sweeney Todd - the demon barber of Fleet Street'
'520*n':'51410688'
'520*t':'Corpse bride'
'520*n':'51410742'
'520*t':'Dark shadows'
'520*n':'51410750'
'534*a':'Af indholdet: Special features'
'652*m':'77.7'
'652*p':'78.81'
'652*v':'5'
'666*s':'musicals'
'666*s':'gyserfilm'
'666*s':'hævn'
'666*s':'mord'
'666*q':'London'
'666*i':'1800-1899'
'666*o':'amerikanske film'
'700*a':'Sondheim'
'700*h':'Stephen'
'700*4':'cmp'
'700*4':'lyr'
'700*4':'ant'
'700*a':'Wheeler'
'700*h':'Hugh'
'700*4':'ant'
'700*a':'Prince'
'700*h':'Harold'
'700*4':'ant'
'700*a':'Bond'
'700*h':'Christopher'
'700*4':'aus'
'700*a':'Wolski'
'700*h':'Dariusz'
'700*4':'cng'
'700*a':'Logan'
'700*h':'John'
'700*4':'aus'
'700*a':'Burton'
'700*h':'Tim'
'700*4':'drt'
'720*o':'Johnny Depp'
'720*4':'act'
'720*o':'Helena Bonham Carter'
'720*4':'act'
'720*o':'Alan Rickman'
'720*4':'act'
'720*o':'Timothy Spall'
'720*4':'act'
'720*o':'Sacha Baron Cohen'
'720*4':'act'
```
