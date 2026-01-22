# Callsign Parser Lookup

## Project Structure
- `CallsignParserLookup/CallSignParser.py` - GUI application (tkinter)
- `CallsignParserLookup/parser.py` - Standalone parser module (reusable library)
- `CallsignParserLookup/cty.dat` - Country prefix database

## parser.py Summary
Standalone call sign parser module that can be used as a library.

### Key Classes/Functions
- `CallSignParser` - Main parser class with cached cty.dat loading
- `parse_callsign(callsign)` - Convenience function returning (prefix, separator, suffix, country, is_valid)

### Exceptions
- `CallSignParserError` - Base exception
- `CtyFileNotFoundError` - cty.dat missing
- `CtyFileReadError` - cty.dat read error
- `InvalidCallSignError` - Invalid input

### Usage
```python
from parser import CallSignParser, parse_callsign

# Simple usage
prefix, sep, suffix, country, valid = parse_callsign("KD4SIR")

# Class usage
result = CallSignParser.parse("G4ABC")
CallSignParser.clear_cache()  # Clear cached cty.dat if needed
```

### Features
- Caches cty.dat on first load (class variable `_cty_cache`)
- Uses `os.path.dirname(__file__)` for reliable file paths
- Input validation (empty, too short, missing letters/digits)
- Proper context manager file handling
