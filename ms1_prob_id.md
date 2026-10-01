# Milestone 1 Problem Identification


## QUESTIONS

### 1) What unknown wrong data is there?

These are wrong data found by reviewing the dataset.
- There are some empty value in the columns.
- Some data contain non-alphabetic characters.
- The data format is not consistent within the same column.
    For example, the data of born format is dd-mm-yy, but some actual data is mm-dd-yy.
- There are 'Error' values that can cause errors in some column.
    For example, the data of pos column of the event_result file contain '#ERROR!'
- Some data contains partial information.
    For example, some data in the competition_data column of the the olympics_games file contain only symbol '-'

These are unknown wrong data that have not identified yet.
- There could be redundant records.
- There might be missing information.
    For example, only year of birth is provided in the birth column.
- There might be some data that don't match the corresponding columns.
- There might be invalid data.
    For example, dataset is supposed to be between 1 to 50, but 100. 
- There might be different ways to represent empty data.
    For example, some column display nothing for the empty data, while others use symbols or words.


### 2) How will wrong/unknown data be handled?

From looking closely at the data stored in the csv files, some of the dates have missing day, month, or year. For example, some athletes have just the year of their birthdate and have missing day and month. These data are considered to be wrong/unknown and reasonable estimates to assume their birthdate, like 01-Jan, will be made instead to make the birthdate complete with all aspects of a date. For athletes that have a missing year in their birthdate, a birth year like 0 could be added to indicate a missing year. 

If any data are missing, then they will remain as an empty string. For duplicate records when we wish to add paris athlete data to the original athlete bio dataset, a set or dict containing ids of the existing athletes could be included, and checks would be performed before adding new athlete data to see if the athlete is already in the original dataset.

Some birthdates contain other strings that do not represent a date. For these cases, it's best to leave it empty as they do not represent a valid date, and assumptions cannot be made about the athlete's birthdate. 

For the new age column in the new_olympic_athlete_event_results.csv file, age is calculated up to the competition dates of the olympics. If the athlete's birthday falls in the range of the competition dates, then calculations would be made for the age to use the birthdate of the previous year before the olympics, which would result in the athlete being 1 year younger in the records.

### 3) How will Paris data be organized? How does this relate to the original data file? How will you determine the duplicate athlete entries?

The new data files will contain clean, non-trivial nor duplicate, and appropriate information (according to their columns) based on 
the original csv files provided; lets remember that the term "clean" refers that all values within a specific column must share 
exactly the same format (e.g. all dates must comply the format dd-Mon-yyyy) and an adequate handling in case of empty fields (e.g. default values). The new data files will contain the EXACT SAME information from the originals once it is fully processed according to the previous mentioned characteristics.  

Similarly, the Paris Olympics 2024 data will be distributed along all the new corresponding files and appended to the end of them as this is the newest fully published data from the Olympics. It should be emphasized that the Milano-Cortina 2026 Olympics will also be handled in this project but only in minimal information as this tournament is currently in progress (by the time of developing this work) and its data is not fully published yet. 

To put some examples into matter, new athletes who competed on their first time in the Olympics at Paris, their information will be added at files olympic_athlete_bio.csv and olympic_athlete_event_results.csv. On the other side if it was an athlete who competed but they were not a first-timer at the Olympics, their data will only be added in the latter file mentioned as their biography (former file) is supposed to be already added. We can evaluate whether an athlete was or pretended to be entered twice by verifying their ID number, this is the safest approach because if we relied typically only on their names, we could risk facing the event of having two or more different athletes with the same names or even other attributes, so their IDs guarantee that this does not occur.


### 4) How will you be able to tell if your application was working? Are there specific records that you can check?
We will ensure that our application is functioning correctly by verifying that it successfully completes each of the tasks defined in the project instructions. The first task involves adding the Paris 2024 data to the main Olympic dataset. In this stage, we must guarantee three essential conditions. First, no duplicate records should be introduced when merging the Paris data with the existing files. For example, the Armenian athlete ALEKSANYAN Artur appears in both datasets, so we must ensure that he is not added twice to olympic_athlete_bio.csv. To achieve this, we will implement a validation function that checks for duplicate athletes before inserting new records.

Second, the task requires maintaining consistency in internal fields such as IDs. If a new athlete from Paris does not have an assigned ID, we may generate one; however, this ID must be applied consistently across all related files. To enforce this, we will create a function that validates the presence and consistency of essential fields—especially IDs—across all datasets.
Third, the Paris data must follow the same formatting conventions as the original dataset. This means we cannot simply append the Paris files directly; instead, we must ensure that all fields match the expected structure and formatting rules. A dedicated validation function will help confirm that the integrated data respects these requirements.

The second task focuses on data cleaning. Once we have a consistent, duplicate‑free dataset, we will apply a series of validation functions to ensure that all fields meet the required formatting standards. For example, we will implement a function that checks whether all date strings follow the required format dd-Mon-yyyy, including the competition date ranges in olympic_games.csv, which must follow dd-Mon-yyyy to dd-Mon-yyyy. We will also create a function to handle missing information by replacing absent values with empty strings, and another validator to ensure that no empty or invalid fields remain after cleaning.

The final task involves adding new information to the dataset. This includes computing and adding an age column to olympic_athlete_event_results.csv, where the age must reflect the athlete’s age at the start of the Olympics, even if their birthday occurs during the event. We will also add the official dates for the Paris 2024 Olympics and the Milano‑Cortina 2026 Winter Olympics to olympic_games.csv. After calculating the ages and inserting the new dates, we can validate the results either through direct inspection using filters or by implementing additional validation functions. 

If all these validation steps (tests) pass successfully, we can confidently conclude that the application is functioning correctly and that the processed dataset is accurate, consistent, and complete.
