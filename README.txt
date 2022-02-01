This folder contains code that gets data regarding financial disclosures from
the Court Listener API

   • main.py: contains driver code that interacts with all the other files. Only file that should be run. When run it will grab all the data and populate output.csv with it
   • auth_token.py: Reads API authentication token.
   • AUTH_TOKEN.txt: Contains API authentication token. Obtain yours from https://www.courtlistener.com/api/rest-info/ and paste it into this file
   • fields.py: contains the code that grabs all the fields from every disclosure
   • lookups.py: contains some extra lookup tables (aside form the ones embedded in fields.py) for the values returned from the API
   • utils.py: contains some utility functions
   • requirements.txt: contains the list of dependencies used. Install them by running pip install -r requirements.txt
   • README.txt: readme in txt format

