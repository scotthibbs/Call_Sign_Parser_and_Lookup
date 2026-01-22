# Call_Sign_Parser_and_Lookup
This can be a standalone program (or used within another program) to parse a
callsign into a prefix, separator, and suffix and also determine the 
country from the prefix. 
Python 3 code to look up amateur radio (ham) call signs from the cty.dat file. 

I had claude code grab ahold of this and this was his upgrade:
- Add ability to click button and update the database. 
Refactor: separate parser logic into standalone module
- Extract all parsing logic from CallSignParser.py into new parser.py module
- parser.py can now be used as a reusable library
- Fix file handle leak: use context manager (with open) instead of manual close
- Fix string formatting bug: separator now displays as "4" not "['4']"
- Add cty.dat caching for improved performance on repeated lookups
- Add proper exception handling with custom exception classes
- Add input validation (empty, too short, missing letters/digits)
- Use os.path.dirname(__file__) for reliable file path resolution
- Fix typo: "seperator" -> "separator" throughout
- Remove unused lastofthelist() method and test code
- Add CLAUDE.md project documentation

If you do use this in another project, or please fork it and/or add your enhancements,
I'd love to see it or your project so I can learn more. 

I wrote this to be used eventually in my other project, FDLog_Enhanced.
Feel free to email scott hibbs at gmail dot com 
73, Scott KD4SIR
