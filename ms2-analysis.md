# Milestone 2 Analysis


## Assumptions and decisions made 

- How did we reconcile data for Paris Olympics with Other data? 

    Chloe Kim: For the NOC data, reconciliation was relatively straightforward. 
    Since the data was in CSV format, I used VLOOKUP to compare the datasets before implementing and verify consistency.
    If a country code already existed in the original dataset, it was not added again.
    Only new NOC entries from the Paris dataset were appended. 
    For athlete data, reconciliation was more complex due to the large dataset and inconsistencies in athlete ID formats.
    Initially, I attempted to match athletes using their IDs as a unique key.
    However, since IDs did not align across datasets, we explored matching based on other attributes such as name, date of birth, height, weight, and country code.
    I considered treating athletes as the same individual if at least two or more attributes matched. However, as a team decision, we ultimately assumed that if athlete IDs were different, they represent different individuals. 
    Therefore, all Paris athlete records were appended depulication based on attributes. 
    We assumed that the Paris dataset follows a similar structure to the original dataset and formatted the data to match it as closely as possible. 

    Erik: For Paris 2024, the row existed in the original file but all date fields were empty. The official dates were researched and hardcoded directly into the program (26-Jul-2024 to 11-Aug-2024). For the competition_date range, two special cases were handled: Tokyo 2020 which was held in 2021 due to COVID-19, detected by checking if the year was already present in the date 
    string; and editions where the start and end dates fall in the same month, where only the day is given for the start date (e.g. "6 – 13 April"), so the month is extracted from the end date and appended to the start date.

    Yuan Jie: In the athlete event results file, athlete result data could be retrieved from multiple files instead of a simple one-to-one match. The original paris athletes.csv file contained athletes that took part in the paris olympics along with the events that they participated in as a list. This meant that we had to parse the paris athletes and iterate through the events column that contained a list of event participated by the athlete and insert them as 2 different records into the final event results file. The paris data also did not have proper formatting for the event name string compared to the original event results data. For example, the "Men's Sabre, Team" event for the Fencing sport had to be changed to match the original data in one single string in the format of "Sabre, Team, Men", which was resolved by appending the event name as one string element. 

    Santiago: Initially, it was thought that the medals for a country were counted per athlete regardless if they belonged to a team sport or not, however this assumption represented a problem when printing the medal results, as the total number of medals for some countries/entities showed an increased ammount different from the real results if fetched in the web (e.g. Japan in 2024 Summer Olympics appearing with 82 instead of 45 total medals which was the correct value). We changed the assumption now as interpreting whenever the athletes within a team sport won a medal, everybody won the same kind of medal hence it is counted as just one medal collectively for the team, thus one medal contribution for the country/entity they represented. In this way the total medal numbers decreased to the correct quantity.

- How did you handle missing data?

    Chloe Kim: For numerical or optional fields such as height and weight, empty values were kept as empty strings rather than assigning default numeric values. For date fields, if the data was missing or invalid, an empty string was used. For incomplete date values, a reasonable estimate was applied where possible. However, if the format could not be recognized, the value was left as an empty string. 

    Erik: Empty date fields were left as empty strings. Dash values "—" used for cancelled games (1916, 1940, 1944) were also converted to empty strings. Dates missing the year (e.g. "6 April") were completed by appending the year from the year column of the same row before parsing.

    Yuan Jie: Athletes without a valid birthdate had an empty field in the athletes bio file. Without a valid year, the age of the athlete could not be calculated, which was why I defaulted to an empty string to make sure the age field for the particular athlete without a valid birthdate was empty and not 0 as it would have a completely different meaning. For those athletes with missing days or months but still had a valid year, proper estimates were made, which allowed the age to be calculated using only the year. For example, an athlete with the birthdate "1990" will be 34 years old even though the birthdate is incomplete.

    Santiago: For retrieving information from other files' rows in order to construct medal_tally.csv, my logic implemented checks to verify emptiness of some attributes from those rows, if the attributes were present in the row, process them, otherwise do nothing. We want medal_tally file to have all values present, even if they are 0 as a default value, but all attributes of the rows must be present at this file (i.e. this: `a,,c,d` cannot happen).

## Data structures used 

- How did we use data structures (built-in or created our own ones)?
  
    Chloe Kim: I used built-in Python data structures such as dictionaries, lists, and index.
    Dictionaries were used to store and map data efficiently. (athlete ID to athlete information, NOC  to country name)
    Lists were used to store rows of data and to construct CSV outputs.

    Erik: create_olympics_games() uses a list of lists to store the olympics_games.csv data. Each inner list is a row where each element corresponds to a column (row[7] = start_date, row[8] = end_date, row[9] = competition_date). The data is manipulated by iterating through each row and replacing the date values with the cleaned versions returned by format_date() and format_date_range ().

    Yuan Jie: When implementing append_paris_medallist_results() and append_paris_athlete_results(), I used built-in python data structures like lists to parse the olympic data, and I used its indices to retrieve data from the csv files. I also used sets and tuples for storing the sport and event for each athlete and mapped them to their athlete_id using a dictionary for faster access times. A dictionary was also used to map gender titles to quickly change the format of the event name in the athlete event results file. 

    Santiago: For implementing populate_medal_tally(), I used dictionariees; for retrieving country name with NOC, tuples; for storing (edition, edition_id), lists; for storing objects or other lists, and sets; for storing tuples. As well I used classes for instantiating Editions, which inside contained a list of Country classes, each one containing relevant data such as the medals, to put it in a phrase it would be seen as:
    "The medal tally file contains the records of each olympics edition, for each edition, it contains records of countries, for each country, it contains records of medals, athletes, and team sports; where if the country's athletes won medals for their team, those medals are only counted as 1 collectively for the country."

- How is the overall data manipulated in general?
    
    Chloe Kim: The first stem to process is to read CSV files and converts the data into a dictionary. And cleans the data to match the format and merges it with the original data file. 

    Yuan Jie: For olympic_athlete_event_results, the data was parsed from the original csv files and read into a 2D array or a list of lists. I passed the list directly to the append_paris_medallist_results() to format and select specific fields using their column indices for the new csv file. The function ensures that data is clean and no duplicates are added to the records of the new csv file. After all paris data are parsed, the paris data are combined with the original file and appended at the end of the original data set and written into a new csv file. 

    Santiago: The data is first read from the respective files, cleaned and ensured it has consistency and empty values handling; where consistency means same formats for each attribute of a row, and emptiness handling is setting default values in case any data is missing of incomplete. After that, it is processed according to the requirements; this can be from copying it, inserting, moving, counting and deducting, among other processes. And finally the results produced are revised to check if all rows are consistent in format and that they do not have any kind of anomalies.

- Why did we choose those data structures? How did we use them?
    
    Chloe Kim: I used built-in Python data structures such as dictionaries, lists, and index.
    Dictionaries were used to store and map data efficiently. (athlete ID to athlete information, NOC  to country name)
    Lists were used to store rows of data and to construct CSV outputs.
    Dictionaries allow for fast data retrieval, making them suitable for processing large datasets. Lists are suitable for exporting in CSV format. Overall, this structure allows for efficient processing or large data while remaining easy to maintain.

    Erik: A list of lists was chosen because the file is small (65 rows) and sequential. Every row needs to be processed in order, so no lookup by key was needed, making a dictionary unnecessary. The cost of iterating is O(65) which is negligible compared to the other files in the project.

    Yuan Jie: I used a dictionary with athlete_id as a key and values that were a set of tuples to hold (sport, event) values because I needed to verify that a similar event record for the same athlete was not previously added already. The set of tuples worked well as an athlete could participate in many events, which justifies the use of a set. The tuple is a hashable value and allowed both sport and event to be compared simultaneously, which eliminates the case where two events have the same name. The set also allowed the use of the `in` operator, which has an `O(1)` average time complexity when looking up a value. 

    Santiago: I especially chose sets to store tuples of (edition, edition_id) because it allowed to quickly verify if a tuple was in this set, without linearly searching, but with O(1) search time, as sets contain unordered items hence are different than lists and very reliable for lookup tasks. This is a similar behaviour for the dictionary where we can use a NOC code in order to quickly retrieve the country name, or in other dictionaries with other values, do the same behaviour very fast. Lists were used mainly to perform linear tasks such as printing an edition and its details to the medal tally, as we need to perform a same task for ALL the items of the list, not only to some of them.


## Data size analysis

- let `n` represent the number of records in the `olympic_athlete_events_results` file
- let `a` represent the number of records in the `olympic_athlete_bio` file
- let `p` represent the number of records in the `paris athletes` file
- let `e` represent the number of records in the `paris events` file
- let `m` represent the number of records in the `paris medallists` file.



#### Runtime to clean all data

Chloe Kim: For the country data, the loadCountryDataAndFormatting and loadParisDataAndFormatting iterate through all rows in the dataset once, resulting in a time complexity of O(n) and O(p). 
For athlete bio data, both function loadBioDataAndFormatting and loadParisBioDataAndFormatting iterate through all rows in the datasets once, resulting in a time complexity of O(n) and O(p).
The function format_birth runs in constant time O(1) per call

Erik: create_olympics_games() uses two sequential loops over the 65 rows of olympics_games.csv. The first loop cleans all date fields using format_date() and format_date_range(). The second loop hardcodes the Paris 2024 dates. Since the file always has a fixed number of rows independent of any other file in the project, the runtime is constant — O(1).

Yuan Jie: For olympic_athlete_event_results, the runtime to clean data and add the extra age column at the end of all records was O(n). When cleaning paris athletes data, the runtime to clean it was O(p). Even though in the append_paris_athlete_results() function, 2 loops were used to iterate through the data set, the events for each record never exceeded 4, which means that the second loop was constant time complexity, O(1). When cleaning paris medallists, the runtime was O(m). Although the function append_paris_medallist_results() used to clean paris medallists data contained a lot of operations, the size of the data, m, was still the dominating factor, which is why the runtime is still O(m).

#### Runtime needed to add paris data into the records
Chloe Kim: For country data, the entire dataset is traversed once using the mergeOlympicsAndParis function, and the time complexity is O(1). Similarly, for player data, dictionary lookup is O(1). On the other hand, the conversion functions convertDictTolist and convertBioToList traverse records once each, so the time complexity is O(n). Since the most important factors are the size of the original dataset (n) and the Paris dataset (p), the total execution time required to add Paris data is O(n+p).

Yuan Jie: The runtime to add paris athletes data is also the same as the runtime to clean the data, O(p). This is because the data is appended after it is cleaned, and appending the data is done with the same function. For the paris medallists data, runtime to add the data is also, O(m). 

#### Runtime needed to generate the medal results for all games

Santiago: The total runtime required to run only `populate_medal_tally()`; which is in charge of creating `new_medal_tally.csv` and processing its corresponding content by taking data from other files as well, in project.py, takes `1.344 seconds` assuming the other files where it extracts information were already created. The medal tally file depends MOSTLY (but not completely) on the file `new_olympic_event_results.csv`, from this file we extract the editions, countries, and types of medals (if they are) per each row, hence it is a linear analysis because we need to verify these previous attributes in the entire file as we make the count of: which editions are present, how many countries for that edition, and how many medals for that country. Similarly, being `m` the total records in `paris/medallists.csv` we can determine that there is a linear complexity analysis towards determining `m`, as this file requires extracting information by each row, in order to populate `new_olympic_event_results.csv`.