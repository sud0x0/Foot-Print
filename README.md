This tool is focused only on passive domain name enumeration via online available databases and tools. The current version of the tool uses,
 - DNSDumpster.com 
 - HackerTarget.com
 - BufferOver.run
 - Shodan.io

**Requirements**

 - Python3
 - Pandas (PIPY Module)
 - bs4 (PIPY Module)
 - Shodan (PIPY Module)

**Process**

This tool will do 

 - A record search (Including Wildcard domains)
 - PTR Record search 
 - MX, NS and TXT data 
 - Getting information about A records via Shodan
 
 **Usage**

 1. Run the setup.py: python setup.py install 
 2. Open the tool: python foot_print.py
 3. -h: will provide information regarding the tool
 4. -n: name of the output file. (This is mandatory)
 5. -d: is to provide a single domain.
 6. -f: is to provide a text file that has a list of domains. (The file should be in .txt format and domain should be listed one after other)

If setup.py does not work (due to PIP issues) install the required modules manually via pip.

**Limitations**

The tool has limitations which derive from above online tools. They are,
 
 - The tool uses DNSDumpster.com as the primary source. Therefore, if the DNSDumpster daily limit exceeded for the IP, the tool will not be able to process the rest of the functions. 
 - The tool will use HackerTarget.com free daily search quota. Also, it can be configured with the API key.
 - Shodan will not work without an API key. Therefore, A Records will not get scanned via Shodan.




