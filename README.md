# Submission for Squirro Application
Name: Mark Neil S. Ocampo
Date: 20/09/2024

# Requirements
Python 3.x
Requests library (already included in the requirements.txt)

# Comments
Based on the provided Task and Appendix Codes, here are my comments:
1. I only followed what is needed to be printed based on the Appendix codes. But there is a commented code to display each of the flat article dictionary if needed.
print(f" - {item['_id']} - {item['headline.main']}")
2. I updated the code for connect function to cater for inc_column and max_inc_value. There is a sample code under __main__ if wanted to use it for testing: This will filter the pub_date based on the date provided. It will be the begin_date in the API parameter.
3. Added flat_dictionary function to create the dictionary with all the data in the json response.
4. getDataBatch is updated to cater for pagination of the API request and handle the article received using the flat_dictionary function.
5. getSchema is changed to use the schema created in the getDataBatch (this is based on the API json response)

# How to Download and Run

1. Download ZIP in github (https://github.com/jamirxp/squirro_python)
2. Copy squirro_python-master.zip to c:/
3. Right click and extract all for squirro_python-master.zip
4. Open Terminal or Command Prompt
5. Make sure you have a python installed on your machine (python --version)
6. Enter "cd C:\squirro_python-master\squirro_python-master" and press Enter
7. Enter "python squirro.py". The python script should start running. 

If there's an error you might need to install requests (pip install requests)