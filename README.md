## Summary
This code reads a CSV file containing a column of keywords and uses the OpenAI API to categorize each keyword into an intention and a stage. It then creates a Pandas DataFrame with the categorized keywords and saves it as a CSV file.

## Code Analysis
### Inputs
- CSV file containing a column of keywords
- OpenAI API key
___
### Flow
1. Read the CSV file and store it in a Pandas DataFrame.
2. Set the OpenAI API key.
3. Initialize variables for counting keywords and batch indexing.
4. Calculate the total number of keywords.
5. Iterate over batches of 100 keywords until all keywords are processed.
6. Convert each batch of keywords to a string.
7. Create a prompt for the OpenAI API using the batch of keywords.
8. Call the OpenAI API to categorize the keywords.
9. Process the categorized keywords and split them into substrings.
10. Assign each substring to temporary variables and append them to corresponding lists.
11. Update the counters.
12. Create a Pandas DataFrame from the lists of categorized keywords.
13. Save the DataFrame as a CSV file.
___
### Outputs
- Categorized keywords saved as a CSV file.
___

### Run 
- To run the script need
  ```shell
  cp .env.local .env
  ```
- Place a ChatGPT Openai key in the .env file for the script to function properly.
- Create a virtual environment and run the command and install all the dependencies
  ```shell
  pip install -r requirements.txt
  ```
- Activate the virtual environment and run the script in the shell.
  ```shell
  python search_intent_to_csv.py
  ```
or the command to install all the tools with poetry install, the auto executes everything alone
  ```shell
    make install
  ```
  
___
