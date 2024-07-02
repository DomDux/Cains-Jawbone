# Cain's Jawbone:  A Novel Puzzle
Cain's Jawbone is a puzzle published in 1935 by Edward Powyss-Mathers, better known by his pseudonym: _Torquemada_.  Powyss-Mathers was a regular contributer to the Observer cryptic crossword, and published Cain's Jawbone in their cryptic crossword anual.

The book consists of 100 pages _"published out of order"_ so the story narrated is almost incomprehensible on the first read.  
The goal of the puzzle was to rearrange the pages of the book to the correct order so the story makes sense, and then to solve the murder mystery(s) it describes!
Supposedly, there are 6 murders of **named characters** with 6 different murderers who are **also named.**

## So what?
Why do we care about this?   

Well, since it's publication in the 1930's until 2020, only 3 people had ever solved the puzzle!  It is supposed to be one of the hardest puzzles put to paper (mostly due to its scale) and solving it carries a certain amount of clout.
Since it's been republished in 2022, there has been a second competition to solve the book, and although numbers are unclear, it appears that many more people have solved it with the help of the internet.

I would also like to solve the puzzle, but without resorting to asking questions on reddit as **that is cheating!**  
Instead, I want to maintain a comprehensive repository of notes and features which I can access on my PC/phone so I don't have to carry 100 of loose sheets of paper with me as I try to solve it.

I want to maintain an app which:
 - Contains the text of the book
 - Allows me to make my own notes about sections of the text
 - Allows me to tag my notes/sections of text
 - Has a log of people, places, events and the relationships between them
 - Gives me the option to rearrange the order of the pages easily

## The Project
I intend to build this app utilising a Flask-MongoDB backend and a React frontend.   
### 1. Scanning the book:   Tesseract OCR
The first thing to do is scan the text of the book.  I have my own copy (which I paid good money for of course) and have taken photos of each of the pages.  These I have scanned and loaded into a folder then used `pytesseract` OCR to get the text of each page and save them as individual `.txt` files

### 2. Initialising the Backend:  SQLite/Mongo DB
It would probably be simplest to use a regular SQLite database for the majority of this to begin with, but I am currious about using NoSQL databases and think this is a good opportunity to try one out.  I also intend to implement a few features, such as tagging data, which I think will be well served by the more flexible schema.

The tables/collections we expect to build are as follows:
 - Users:  User IDs and passwords so there can be some authentication for this app
 - Pages:  The data for the actual pages of the book.  Just page number and the text.  Could add successor for when we KNOW a certain page comes immediately after the page
 - Note:  User created notes.  Should have content, higlighted_text, page, people, locations, events, tags
 - People:  Identified people.  Just have text for descriptions and notes.
 - Locations: Identified locations.  Similar to people
 - Events:  Needs a timestamp
 - Relations: related entities, and relation (e.g. `'start_id':100, 'start_type':'person', 'end_id':101, 'end_type':'person','relation':'mother'` or `'start_id':100, 'start_type':'person','end_id':12, 'end_type':'location' 'relation':'home'`)

I will start by creating a SQLite database to do a simple relational database version.  If that is straightforward, I can explore NoSQL options at a later date.

### 3. Flask API
Once we have a DB set up, we start a Flask instance and use it to create an API to integrate with a React interface.

Remember, Flask creates the app from the `.flaskenv` file so we need to provide this in the root directory
```
FLASK_APP={{ api.py }}
FLASK_ENV=development
```
which will then mean when we run 
```
flask run
``` the code will run on `localhost::5000` so we can test the endpoints.

### 4. React Frontend
I am following most of the steps laid out in (this tutorial)[https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project] for creating a web app with a Flask backend and React front-end.
