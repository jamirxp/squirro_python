# Submission for Squirro Application
Name: Mark Neil S. Ocampo
Date: 20/09/2024

# Requirements
Python 3.x
Requests library (already included in the requirements.txt)

# Comments
Based on the provided Task and Appendix Codes, here are my comments:
1. I only followed what is needed to be printed based on the Appendix codes
print(f" - {item['_id']} - {item['headline.main']}")
2. I notice as well that connect and getSchema function are not being used. I did not do any changes to the function since it is not part of the requirements.
3. In the getSchema function, some are incorrect like id, based on the json response from API, it is "_id". But same on #2 i did not do any changes.
4. I notice too that the batch printing is never ending. It is best to add a max batches. I did not add these, because it is not part of requirements.

# How to Download and Run

1. Download ZIP in github (https://github.com/jamirxp/squirro_python)
2. Copy squirro_python-master.zip to c:/
3. Right click and extract all for squirro_python-master.zip
4. Open Terminal or Command Prompt
5. Make sure you have a python installed on your machine (python --version)
6. Enter "cd C:\squirro_python-master\squirro_python-master" and press Enter
7. Enter "python squirro.py". The python script should start running. 

If there's an error you might need to install requests (pip install requests)