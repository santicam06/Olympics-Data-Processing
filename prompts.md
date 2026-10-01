# Prompts log

This file logs the tool/prompts you used and the results.  A small note on whether it was successful, choices you made and what was used.

## Example (can be deleted):

|AI tool name|prompt | result | alterations |
|---|---|---|---|
|gh copilot|what do you use to read in csv files in python| csv module or pandas | rejected pandas as it is not allowed |
|gh copilot|write a function that is passed the name of a csv file and will return the data set of that file| read_csv_file(file_name) | updated to account for utf-8 formatting |

## Team-Member1 - Chloe Kim 


|AI tool name|prompt | result | alterations |
|---|---|---|---|
|ChatGPT  | What is the best tool or container to store massive dataset in python?  | List of objects(most common), Dict(best for look up), Generator/streaming(if dataset is large but still local), SQLite(very important)   | I chose to use lists and dictionaries because I learned about table structures in class, and dictionaries is efficient data searching. Also, it says that the Generator fits on a large dataset but I rejected to use it because I haven't learnt it.  |
|ChatGPT  | How to create new csv file after reading a file?  | create a new CSV using the csv module -> csv.writer | None  |
|Git Copliot  | I saved an entire row from a CSV file to a rowData object, then save it to objects and print it to check the data saved. Why does obj[0].rowData[0] only return one column?  | This is because rowData actually stores an entire row read from a CSV file in list format. When reading a CSV file, each row is stored as a list, and each element in the list corresponds to a column. | None  |
|Chat GPT  | The original dataset stores birth dates in the format "dd-Mon-yy", How can I convert various data formats (including year-only) to match this original format, while handling missing or invalid values?  | Convert everything to the original dataset’s format with these rules: Target format: dd-Mon-yy Missing or invalid values: return "" Year-only values like 2001: convert to 01-Jan-01 ISO values like 2001-04-09: convert to 09-Apr-01 Two-digit years should be interpreted carefully so future years do not appear by mistake | None |
|Chat GPT| return f"01-Jan-{date_str}" what does this part do?  | That line: return f"01-Jan-{date_str}" means: 👉 “If only the year is given, make up a full date using Jan 1 of that year.” | None |
|Chat GPT| Is using class for this project not helpful for the complexity?  | 👉 Yes — using classes is not very helpful for improving time complexity in this project. | I removed the use of classes and switched to using lists so that the data can be accessed more easily. |
| Chat GPT  | for noc, country in countries.items(): data_set.append([noc, country]) - How can I get each data without using .list()  | This loop iterates through each key in the countries dictionary. For each noc (key), it retrieves the corresponding country name using countries[noc]. Then, it appends both the NOC and the country name as a new row in the data_set list. for noc in countries:country = countries[noc]  data_set.append([noc, country])| None  |
| Chat GPT | The CSV file already has column headers. Am I allowed to change them, or should I keep them as they are? I was also wondering if it would be better to remove the headers entirely. In that case, is there still any benefit to using a dictionary structure?  | you should keep the original column headers as they are unless the instructions explicitly allow you to modify them. The headers are important because they define the structure and meaning of each column, and changing or removing them could make the data inconsistent with the expected format. | None |
| Chat GPT  | How to remove space from csv file in python? |  .strip() removes whitespace (spaces, tabs, newlines) from the beginning and end of a string. | None |


## Team-Member2 - Erik Chacon 


| AI tool name | prompt | result | alterations |
|---|---|---|---|
| Claude | "Asked for guidance on how to implement create_olympics_games() for MS2" | Claude explained the 3 steps needed: read file, clean dates, write file. Also identified 7 data issues in olympics_games.csv | Used the structure suggested but implemented the code myself step by step |
| Claude | Uploaded olympics_games.csv and asked Claude to find errors, inconsistencies and formatting issues in the file | Claude identified 7 issues: missing year in start_date and end_date, incomplete date ranges in competition_date, Tokyo 2020 edge case with year 2021, cancelled games showing dash instead of empty string, leading/trailing spaces, Paris 2024 missing dates, and Milano-Cortina 2026 needing formatting | Used the findings to plan and write the cleaning logic in create_olympics_games(), format_date() and format_date_range() |
| Claude | "datetime.strptime how does it work?" | Claude explained that strptime converts a string to a datetime object using format codes (%d, %B, %Y) and that the string and format must match exactly | Used the explanation to understand and write format_date() correctly |
| Claude | "datetime.strftime - asked about the opposite function" | Claude explained that strftime converts a datetime object back to a string using the same format codes, outputting the desired dd-Mon-yyyy format | Used directly to return the formatted date string in format_date() |
## Team-Member3 - Yuan Jie Wong


|AI tool name|prompt | result | alterations |
|---|---|---|---|
| ChatGPT | How do I import python files and use the functions within them? | Use the import keyword followed by the file name. When invoking the functions in the module, the file name of the module must be added as a prefix to the function call  | None |
| ChatGPT | Is python list slicing's first argument inclusive? | Yes, the first argument in the syntax specifies the start and is inclusive. For example, array[2:] means that it starts from the element at index 2. | None |
| ChatGPT | when the end index is not provided, is it to the end of the list by default? | Yes, if the end index is omitted, python defaults to the length of the list. For example, array[2:] means that it starts from the element at index 2 and includes all remaining elements of the array. | None |
| ChatGPT | Is the python `in` operator O(1) in time complexity? | Depends on the data structure. `in` operator performs linear search on lists, tuples, and strings, which makes it O(n) complexity. However, sets and dicts are O(1) complexity. | In problem identification, I made plans to use a dict or a set to store ids of athletes to keep track of existing ids in the original dataset and check using the `in` operator to see if the athlete in the new paris records have already been added or not. This makes it O(1) complexity and does not slow down our program when searching for a specific athlete record among 150k+ records. |
| ChatGPT | does python have a method to separate parts of a string with a delimiter? | yes, python has a split() method to divide strings into a list. For example, string.split(delimiter) will split the string into an array where each element is the part of the string separated by the delimiter specified. | used medal.split() because default delimiter is whitespace. For example, "Gold Medal" will be split into ["Gold", "Medal"]. |
| ChatGPT | Will title() work on a string with spaces in between | Yes, the starting of each word will be capitalized and the rest of the word will be lower case. | None |
| ChatGPT | what is the syntax for string join() method in python | 'separator'.join(iterable). For example, if you have an array or a list of values, ["I", "want", "a", "Burger"]. Using the code ' '.join(["I", "want", "a", "Burger"]) will return the string "I want a Burger". | None |
| ChatGPT | does strip work for multiple characters | Yes, the strip() method accepts a string containing multiple characters, and treats the string as individual characters to be removed from the beginning and end of a string. | None |
| ChatGPT | are set O(1) access times with in operator | Yes, in python checking if an item exists in a set using the in operator is O(1) time complexity on average. | Use set with tuples in order to store both event and sport. |
| ChatGPT | are tuples hashable? | Yes, tuples are hashable because they are immutable objects just like strings and integers. | Since sets require immutable objects in order for it to be hashable and stored, a tuple was perfect for my case with sport and event. |
| ChatGPT | Can sets be initialized with {}? | Yes, as long as it is initialized with values. For empty sets, set() must be called. {} could be used if initialized with starting values. For example, {1, 2, 3} is a set and not a dictionary even though it is surrounded by curly braces because it does not contain colons.  | Since I will be initializing a set with a starting tuple of (sport, event) if a new sport and event is found for an athlete, I will be using the curly braces for initialization. |
| ChatGPT | How to append items into a set in python? | Python uses the add() method for adding a single item to a set.  | None. |

## Team-Member4 - Santiago Camacho 


|AI tool name|prompt | result | alterations |
|---|---|---|---|
| GPT-4.1  |If we split a row into an array, each index containing a property from the row, and we find that the row contains some empty properties, then by using .split() this will set those empty properties as empty indices?   | Yes, when you use the .split() method on a string (such as a CSV row), empty properties between delimiters will result in empty string elements in the resulting array.  | None  |
| GPT-4.1 | Is there a built in method like find() that can allow me to verify if row[2] (the country NOC) exists in the olympics_country file, and from that, get the full name of the country? |Python lists do not have a built-in method like find() that returns an element based on a condition. However, you can use a dictionary for efficient lookup.

Since your olympics_country file is loaded as a list of lists, you can convert it to a dictionary for fast access|None|
