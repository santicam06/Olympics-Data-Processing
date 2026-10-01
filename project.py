# Feel free to add additional python files to this project and import
# them in this file. However, do not change the name of this file
# Avoid the names ms1check.py and ms2check.py as those file names
# are reserved for the autograder

# To run your project use:
#     python runproject.py

# This will ensure that your project runs the way it will run in the
# the test environment


# Libraries
import csv
from datetime import datetime
from typing import List


# This function reads a csv file and return a list of lists
# each element of the returned list is a row in the csv file
# The first row is the header row
def read_csv_file(file_name):
    data_set = []
    with open(file_name, mode='r', encoding="utf-8-sig") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data_set.append(row)
    return data_set

# This function writes out a list of lists to a csv file.
# each element of the list is a row in the csv file
# The first row is the header row
def write_csv_file(file_name, data_set):
    with open(file_name, mode='w', newline='', encoding="utf-8-sig") as file:
        csv_writer = csv.writer(file)
        for row in data_set:
            csv_writer.writerow(row)


# ---------------------------------------------------------- GROUP CUSTOM FUNCTIONS ----------------------------------------------------------


# This function creates the new_medal_tally.csv  
# file with the appropriate header. 
# It does not receive nor return anything.
# (Santiago) 
def create_medal_tally():
    data_header = ["edition", "edition_id", "Country", "NOC", "number_of_athletes",
                   "gold_medal_count", "silver_medal_count", "bronze_medal_count", "total_medals"]

    with open("new_medal_tally.csv", mode='w', newline='', encoding="utf-8-sig") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(data_header)


class CountryResult:
        def __init__(self, noc, name):
            self.noc = noc
            self.name = name            # Country name
            self.gold_medals = 0
            self.silver_medals = 0
            self.bronze_medals = 0
            self.total_medals = 0
            self.ids_athletes: set[str] = set()             # A country has participant athletes
            self.num_athletes = 0
            self.team_sports_ids: set[str] = set()          # Used to count team medals as just 1 and not per every team member
    
class Edition:
    def __init__(self, edition_name, edition_id):
        self.name = edition_name
        self.id = edition_id
        self.countries: List[CountryResult] = []            # An edition has participant countries 


# Helper function, adds the athlete if applicable
# and the medal data to the passed country
# (Santiago)
def add_athlete_N_medal(
    row: list[str],                 # Current row being parsed
    country: CountryResult          # Country to which add data 
):
    # Add an athlete
        if row[7]:
            athlete_id = row[7]
            # Verify that athlete is not present yet
            if athlete_id not in country.ids_athletes:
                country.num_athletes += 1
                country.ids_athletes.add(athlete_id)

        # Add medal of the row's athlete to this current country
        if row[9]:
            # If current row not team sport
            if row[10].lower() == "false":
                # Check case insensitive and trimmed whitespaces
                match row[9].lower().strip():
                    case "gold":
                        country.gold_medals += 1
                        country.total_medals += 1
                    case "silver":
                        country.silver_medals += 1
                        country.total_medals += 1
                    case "bronze":
                        country.bronze_medals += 1
                        country.total_medals += 1

            elif row[10].lower() == "true":
                if row[5] and row[5] not in country.team_sports_ids:
                    
                    # Add the result_id of row, represents the event done in the row (e.g Soccer Women)
                    country.team_sports_ids.add(row[5])
                    match row[9].lower().strip():
                        case "gold":
                            country.gold_medals += 1
                            country.total_medals += 1
                        case "silver":
                            country.silver_medals += 1
                            country.total_medals += 1
                        case "bronze":
                            country.bronze_medals += 1
                            country.total_medals += 1


# Helper function, instantiates an Edition object and populates all data from the received row
# Understand register as adding a new edition that needs to be (and hasn't been yet) printed in medal_tally.csv
# IMPORTANT: When calling this function, we asume that the country of the row parameter, forcely needs
# to be registered as well, because is the first data instance of this edition, there was nothing before.
# (Santiago)
def register_edition(
    edition_name,            
    edition_id, 
    row: list[str],         # Current row being parsed
    country_dict: dict      # key: NOC; value: country_name
) -> Edition :

    if edition_name and edition_id:
        ed = Edition(edition_name, edition_id)
    else: raise ValueError('register_edition() says -> Please provide edition_name and id.') 

    # Verify that the NOC of current row is valid 
    noc = row[2]
    if noc and noc in country_dict:
        country_name = country_dict[noc]
        # The country of the current row 
        row_country = CountryResult(noc, country_name)

        add_athlete_N_medal(row, row_country)

        # Add the new country to the list
        ed.countries.append(row_country)

    # Returns the registered edition
    return ed
        

# Helper function, used when there is an edition already registered 
# Understand already registered as if we already printed at least one row 
# of a specific edition in medal_tally.csv
# Adds new data for this edition 
# (Santiago)
def add_data_edition(
    editions_tallies: List[Edition],                    # Stores all Olympics editions
    existent_ed_idx: int,                               # Index of edition in edition_tallies
    row: list[str],                                     # Current row being parsed
    country_dict: dict,                                 # key: NOC; value: country_name
    countries_by_ed: dict[int, dict[str, int]]          # key: edition idx; value: dict of countries as {key: noc; value: idx}
    ):

    ed = editions_tallies[existent_ed_idx]

    # Verify that the NOC of current row is valid 
    noc = row[2]
    if noc and noc in country_dict:
        country_name = country_dict[noc]

        # Get the countries dict of this row's edition
        # Variable is a reference of the actual countries dict stored in countries_by_ed
        ed_countries_dict = countries_by_ed.setdefault(existent_ed_idx, {})  # {} default value, if no countries dict found in edition

        # Get the index of the country by noc
        is_registered = ed_countries_dict.get(noc, -1)

        # If country of row not registered in this edition
        if is_registered == -1:
            # A new country must be registered in this edition
            new_country = CountryResult(noc, country_name)

            add_athlete_N_medal(row, new_country)

            # Add the new country to the list
            ed.countries.append(new_country)

            # Keep dict synchronized with previous append
            ed_countries_dict[noc] = len(ed.countries) - 1
        else:
            # The country already exists in ed.countries, process the rest of the current row
            if is_registered > -1:
                existent_country = ed.countries[is_registered]
                add_athlete_N_medal(row, existent_country)
                

# This function inserts ALL the necessary data to new_medal_tally.csv file
# which is as well created here
# This data comes from the new_****.csv files. 
# This function uses helpers which can be found RIGHT BEFORE of this one.
# (Santiago)
def populate_medal_tally():

  # PRE. Create the file with just header 
    create_medal_tally()

  # 1. Get all editions and edition_id

    # Set of tuples as (edition_name, edition_id)
    # Sets provide unordered items for O(1) lookup, no duplicates
    editions = set()
    with open("new_olympics_games.csv", mode='r', encoding="utf-8-sig") as file:
        csv_reader = csv.reader(file)
        # Skip header
        next(csv_reader)                
        for row in csv_reader:
            edition = row[0]
            edition_id = row[1]
            editions.add((edition, edition_id))

  # 2. Read files
    events_set = read_csv_file("new_olympic_athlete_event_results.csv")
    countries_set = read_csv_file("new_olympics_country.csv")

  # 3. FOR EACH edition, determine results by EACH country
    
    # Convert country list to a dict for fast lookup, header NOT included
    # Trim quotes and whites for all country names (e.g. " Hong Kong, China  ")
    country_dict = {row[0]: str(row[1]).strip() for row in countries_set[1:]} 


    # Contains records for each edition
    editions_tallies: List[Edition] = []
    
    # key: (edition_name, edition_id); value: idx of edition in edition_tallies
    editions_dict: dict[tuple[str, str], int] = {}
    # key: edition idx; value: dict of countries as {key: noc; value: idx}
    countries_by_ed: dict[int, dict[str, int]] = {}

    # For each row of events_set
    for i in range(1, len(events_set)):
        row = events_set[i]
        # Verify this row belongs to a valid Olympics edition
        if (row[0], row[1]) in editions:

            edition_name = row[0]
            edition_id = row[1]
            key = (edition_name, edition_id)

            # Get edition index
            is_registered = editions_dict.get(key, -1)

            # If edition of row is not registered
            if is_registered == -1:
                # Register a new Edition to be added to the tallies, and process rest of current row
                ed : Edition = register_edition(edition_name, edition_id, row, country_dict)

                if ed:
                    editions_tallies.append(ed)

                    # Get index of this ed in edition_tallies
                    existent_ed_idx = len(editions_tallies) - 1
                    # Store it in dict
                    editions_dict[key] = existent_ed_idx

                    # Initialize countries dict for this edition
                    countries_by_ed[existent_ed_idx] = {

                        # key: noc; value: country idx (of ed.countries list) 
                        c.noc: i for i, c in enumerate(ed.countries)
                    }
            else:
                # The edition already exists in edition_tallies, process the rest of the current row
                if is_registered > -1:
                    add_data_edition(
                    editions_tallies,
                    is_registered,
                    row,
                    country_dict,
                    countries_by_ed
                )
        

  # 4. FOR EACH edition, print data into medal_tally.csv by EACH country

    with open("new_medal_tally.csv", mode="a", newline="", encoding="utf-8-sig") as file:
        csv_writer = csv.writer(file)
        for ed in editions_tallies:
            for c in ed.countries:
                # Insert all necessary data (in same order as file header) into array
                row = [
                    ed.name,
                    ed.id,
                    c.name,
                    c.noc,
                    c.num_athletes,
                    c.gold_medals,
                    c.silver_medals,
                    c.bronze_medals,
                    c.total_medals,
                ]
                csv_writer.writerow(row)



# Gender dictionary for formatting event names
# (Yuan Jie Wong)
gender = {
    "Men's": "Men",
    "Women's": "Women",
    "Mixed": "Mixed"
}

# This function adds a new column header to a specified data_set parameter.
# The header row is updated with the new col_name parameter at the end.
# The function does not return anything.
# (Yuan Jie Wong)
def append_col(data_set, col_name):
    data_set[0].append(col_name)

# This function finds the maximum edition id from the data set.
# The data set passed to the function is in the olympic athlete event results format.
# The function returns the maximum edition id in the data set.
# (Yuan Jie Wong)
def find_max_id(data_set, index):
    curMax = 0

    for row in data_set[1:]:
        curMax = max(int(row[index]), curMax)

    return curMax

# This function adds the ages of the athletes for each record in the 
# olympic_athlete_event_results data_set at the end if the athlete
# has a valid birth date. Otherwise, it appends an empty string to
# signify no age.
# The function does not return anything.
# (Yuan Jie Wong)
def add_age(data_set, bio_set):
    birth_dates = {}

    for i in range(1, len(bio_set)):
        # map each athlete id to their own birthdate for fast indexing
        date_arr = bio_set[i][3].split('-')
        if len(date_arr) == 3:
            year_str = date_arr[2]
        else:
            year_str = ""

        if year_str:
            birth_dates[bio_set[i][0]] = int(year_str)

    for i in range(1, len(data_set)):
        # search for the athlete's birthday
        athlete_id = data_set[i][7]

        # make sure athlete_id exists before we attempt to get their birthdate
        if athlete_id in birth_dates:
            year = birth_dates[athlete_id]

            data_set[i].append(2024 - year)
        else:
            data_set[i].append("")


# This function formats the event string of paris athlete event results
# for the Fencing sport to match the original athlete event results data set.
# This function returns the formatted string.
# (Yuan Jie Wong)
def format_fencing(event):
    event_string = ""

    event_string += event[1] + ", " + ' '.join(event[2:]) + ", "

    if event[0] in gender:
        event_string += gender[event[0]]
    else:
        event_string += event[0]
    
    return event_string

# This function formats the event string of paris athlete event results
# for the Swimming sport to match the original athlete event results data set.
# This function returns the formatted string.
# (Yuan Jie Wong)
def format_swimming(event):
    event_string = ""

    event_string += ' '.join(event[1:])
    event_string = event_string.replace('0m', '0 metres')

    if event[0] in gender:
        event_string += ", " + gender[event[0]]
    else:
        event_string += ", " + event[0]
    
    return event_string

# This function formats the event string of paris athlete event results
# for the Judo sport to match the original athlete event results data set.
# The function accepts an array of strings representing words in the event
# delimited by spaces.
# This function returns the formatted string.
# (Yuan Jie Wong)
def format_judo(event):
    weight_class = {
        "-60 kg": "Extra-Lightweight",
        "-66 kg": "Half-Lightweight",
        "-73 kg": "Lightweight",
        "-81 kg": "Half-Middleweight",
        "-90 kg": "Middleweight",
        "-100 kg": "Half-Heavyweight",
        "+100 kg": "Heavyweight",
        "-48 kg": "Extra-Lightweight",
        "-52 kg": "Half-Lightweight",
        "-57 kg": "Lightweight",
        "-63 kg": "Half-Middleweight",
        "-70 kg": "Middleweight",
        "-78 kg": "Half-Heavyweight",
        "+78 kg": "Heavyweight"
    }
    event_string = ""

    event_string += ' '.join(event[1:])
    if event_string in weight_class:
        event_string = weight_class[event_string]
    
    event_string += ", " + event[0]

    return event_string

# This function formats the event string of paris athlete event results
# for the 3x3 Basketball sport to match the original athlete event results data set.
# This function returns the formatted string.
# (Yuan Jie Wong)
def format_3x3(event):
    event_string = "3x3 Basketball, " + event[0]

    return event_string

# This function formats the event string of paris athlete event results
# for the Artistic Gymnastics sport to match the original athlete event 
# results data set.
# This function returns the formatted string.
# (Yuan Jie Wong)
def format_art_gymnastics(event):
    event_string = ""

    event_string += ' '.join(event[1:])

    if event_string == "Pommel Horse":
        event_string = "Pommelled Horse"
    elif event_string == "Vault":
        event_string = "Horse Vault"
    elif event_string == "Team":
        event_string = "Team All-Around"
    elif event_string == "All-Around":
        event_string = "Individual All-Around"
    
    if event[0] in gender:
        event_string += ", " + gender[event[0]]
    else:
        event_string += ", " + event[0]
    
    return event_string

# This function adds paris_events to the end of the new_olympic_athlete_event_results.csv data set 
# parameter. data_set and paris_events parameters are both of type list 
# of lists that hold string values. 
# data_set contains the original athlete event results and paris results
# contains the data for the events.csv file. 
# The function returns 2 dictionaries containing information that maps athlete id to sport and event, 
# and event to the corresponding calculated result id.
# (Yuan Jie Wong)
def append_paris_medallist_results(data_set, paris_results):
    edition_id = find_max_id(data_set, 1) + 1
    result_id = find_max_id(data_set, 5)

    medal_pos = {
        "Gold": 1,
        "Silver": 2,
        "Bronze": 3
    }

    athletes = {}
    event_result_dict = {}

    for i in range(1, len(paris_results)):
        row = ["2024 Summer Olympics", edition_id]
        athlete_birth_date = paris_results[i][17].split('-')
        
        # append country code
        row.append(paris_results[i][5])

        # append sport/discipline
        sport = paris_results[i][13]
        row.append(sport)

        event = paris_results[i][14]

        # determine if the event result_id should be incremented
        prev_event = paris_results[i-1][14]
        prev_sport = paris_results[i-1][13]
        if sport != prev_sport or event != prev_event:
            result_id += 1
        
        # keep track of athletes and their sport and events
        athlete_id = paris_results[i][18]
        if athlete_id in athletes:
            athletes[athlete_id].add((sport, event))
        else:
            athletes[athlete_id] = {(sport, event)}

        # map events with their result_id
        if event not in event_result_dict:
            event_result_dict[event] = result_id

        # append event
        event = event.split()
        if sport == "Fencing":
            row.append(format_fencing(event))
        elif sport == "Swimming":
            row.append(format_swimming(event))
        elif sport == "Judo":
            row.append(format_judo(event))
        elif sport == "3x3 Basketball":
            row.append(format_3x3(event))
        elif sport == "Artistic Gymnastics":
            row.append(format_art_gymnastics(event))
        else:
            if event[0] in gender:
                event_string = ' '.join(event[1:]) + ", " + gender[event[0]]
            else:
                event_string = ' '.join(event[1:]) + ", " + event[0]

            row.append(event_string)

        # append result id
        row.append(result_id)

        # append name
        row.append(paris_results[i][3].title())

        # append athlete_id
        row.append(athlete_id)

        medal = paris_results[i][1].split()[0]
        # append pos
        row.append(medal_pos[medal])

        # append medal
        row.append(medal)

        # append isTeam
        row.append(paris_results[i][19] != "")

        # append age
        row.append(2024 - int(athlete_birth_date[0]))

        data_set.append(row)
    
    return athletes, event_result_dict

# This function adds paris athletes to the end of the new_olympic_athlete_event_results.csv data set 
# parameter. paris_athletes of type list of lists that hold string values. 
# athletes_dict contains athlete_ids with their corresponding sports and events as tuples.
# event_res_dict maps events of paris olympics with their corresponding calculated result id 
# The function returns nothing.
# (Yuan Jie Wong)
def append_paris_athlete_results(data_set, paris_athletes, athletes_dict, event_res_dict):
    cur_res_id = max(event_res_dict.values())

    for i in range(1, len(paris_athletes)):
        sport = paris_athletes[i][15].strip("[]'")
        events = paris_athletes[i][16].strip("[]").split(", ")
        events = [event.strip("\"\' ") for event in events]

        a_id = paris_athletes[i][0]

        # check if the event for the athlete is already included 
        for event in events:
            exists = False
            if a_id in athletes_dict and (sport, event) in athletes_dict[a_id]:
                exists = True
            
            if not exists:
                row = ["2024 Summer Olympics", 63]
                athlete_birth_date = paris_athletes[i][17].split('-')
                result_id = 0

                if event in event_res_dict:
                    result_id = event_res_dict[event]
                else:
                    cur_res_id += 1
                    result_id = cur_res_id
                    event_res_dict[event] = result_id
                
                # append country code
                row.append(paris_athletes[i][7])

                # append sport/discipline
                row.append(sport)
                
                # append event
                ev_arr = event.split()
                if sport == "Fencing":
                    row.append(format_fencing(ev_arr))
                elif sport == "Swimming":
                    row.append(format_swimming(ev_arr))
                elif sport == "Judo":
                    row.append(format_judo(ev_arr))
                elif sport == "3x3 Basketball":
                    row.append(format_3x3(ev_arr))
                elif sport == "Artistic Gymnastics":
                    row.append(format_art_gymnastics(ev_arr))
                else:
                    if ev_arr[0] in gender:
                        event_string = ' '.join(ev_arr[1:]) + ", " + gender[ev_arr[0]]
                    else:
                        event_string = ' '.join(ev_arr[1:]) + ", " + ev_arr[0]
               
                    row.append(event_string)

                # append result id
                row.append(result_id)

                # append name
                row.append(paris_athletes[i][2].title())

                # append athlete_id
                row.append(a_id)

                # append pos
                row.append("")

                # append medal
                row.append("")

                # append isTeam
                row.append("False")

                # append age
                row.append(2024 - int(athlete_birth_date[0]))

                data_set.append(row)

# This function sorts the olympics countries in ascending order of country using merge
# sort. 
# The function recursively calls itself until the list is empty or has one element remaining
# and calls merge, which merges the two halves of the current recursive call in ascending 
# order.
# The function returns a sorted list of the olympic country data set.
# (Yuan Jie Wong)
def sort_country(countries):
    if len(countries) <= 1:
        return countries

    mid = len(countries) // 2
    left_arr = sort_country(countries[:mid])
    right_arr = sort_country(countries[mid:])

    return merge(left_arr, right_arr)

# This function is a helper function for sort_country, which is a merge sort.
# This function merges two lists of lists in ascending order. Each element of
# the lists is a list of noc and country, [noc, country]. This function selects the smaller
# country string lexicographically and appends the list, [noc, country], to the result
# list.
# (Yuan Jie Wong)
def merge(l_arr, r_arr):
    res = []
    l = 0
    r = 0

    while l < len(l_arr) and r < len(r_arr):
        # compare country name lexicographically
        if l_arr[l][1] < r_arr[r][1]:
            res.append(l_arr[l])
            l += 1
        else:
            res.append(r_arr[r])
            r += 1
    
    return res + l_arr[l:] + r_arr[r:]

"""
This function converts a date string to the format dd-Mon-yyyy.
The function accepts a date_str parameter of type string and a year parameter of type string.
The original data has inconsistent date formats that need to be cleaned:
    - Dates missing the year:       " 6 April"      -> "06-Apr-1896"
    - Dates already with year:      "23 July 2021"  -> "23-Jul-2021"
    - Empty or invalid values:      "" or "—"       -> ""
The year parameter is used when the year is missing from the date string.
The function returns the formatted date string.
"""

# Erik Chacon
def format_date(date_str, year):
    date_str = date_str.strip()  # to remove leading and trailing spaces
    # Handle empty or invalid values first
    if date_str == "" or date_str == "—":
        return ""
    
    # We divide the string into a list of strings Ex: " 6 April" -> ["6", "April"]
    strings_division = date_str.split()

    # if lenght is 3, we already have the year in the string, so we can ignore the year parameter and use the year in the string.
    if len(strings_division) == 3:
        date = datetime.strptime(date_str, "%d %B %Y") # strptime is used to convert a string to a datetime object, we specify the format of the string we are trying to convert. In this case, we have day, month and year in the string, so we use "%d %B %Y" as the format.
        # %d day, %B complete month name, %Y year with 4 digits, %b abbreviated month name.
        return date.strftime("%d-%b-%Y") # strftime is the oppsite, we convert date into a string
    else:
        # if lenght is 2, we have day and month, so we need to add the year parameter.
        date_str_with_year = f"{date_str} {year}"
        date = datetime.strptime(date_str_with_year, "%d %B %Y")
        return date.strftime("%d-%b-%Y")
    

"""
This function formats a date_range_str parameter of type string into the dd-Mon-yyyy to dd-Mon-yyyy format.
The function accepts a date_range_str parameter of type string and a year parameter of type string.
This function calls format_date to format the start and end dates individually.
Examples:
    "6 – 13 April" + "1896"        -> "06-Apr-1896 to 13-Apr-1896"
    "14 May – 28 October" + "1900" -> "14-May-1900 to 28-Oct-1900"
    "21 July – 8 August 2021"      -> "21-Jul-2021 to 08-Aug-2021"
    "" or "—"                      -> ""
The function returns the formatted date range string.
"""
# Erik Chacon
def format_date_range(date_range_str, year):
    date_range_str = date_range_str.strip() # to remove leading and trailing spaces
    # Handle empty or invalid values first
    if date_range_str == "" or date_range_str == "—":
        return ""
    # We divide the string using the "-". Ex: " 6–8 April" -> ["6", "8 April"]
    strings_division = date_range_str.split("–")
    
    # If we don't have exactly 2 parts separated by –, return empty string
    if len(strings_division) != 2:
        return ""
    
    # Now we must handle the format of each string separately
    start_str = strings_division[0].strip() # to remove leading and trailing spaces of the first string
    end_str = strings_division[1].strip() # to remove leading and trailing spaces of the second string

    # Special case: Tokyo 2020 was held in 2021 due to the COVID-19 pandemic.
    # end_str = "8 August 2021" -> len = 3, year is already in the string
    tokyo_case = end_str.split()
    if len(tokyo_case) == 3:
        actual_year = tokyo_case[2]  # year is the third element
    else:
        actual_year = year
    
    # now  we can format the end date
    end_date = format_date(end_str, actual_year)


    """
    Special case: 
    In most cases where start and end dates are in different months, we have day and month.
    But in cases where start and end dates fall in the same month, the start string only has the day.
    Example: "6 – 13 April" -> start_str = "6", end_str = "13 April"
    So we need to extract the month from end_str and add it to start_str.
    """
    if len(start_str.split()) == 1: # if we only have the day
        temp = end_str.split()
        month = temp[1]  # second element is always the month
        start_str = start_str + " " + month
    
    # now we can format the start date
    start_date = format_date(start_str, actual_year)

    return f"{start_date} to {end_date}"


# we create this function to generate a new csv file with the same data as the original csv file, but with the date column formatted in a different way. We will call the format_date and format_date_range functions to do this.
"""
def create_olympics_games(file_name):
    data_set = read_csv_file(file_name)
    write_csv_file("new_olympics_games.csv", data_set)
"""
# Erik Chacon
def create_olympics_games(file_name):
    data_set = read_csv_file(file_name)
    # read_csv_file returns a list of lists, where each list is a row, starting at index 0 (header)
    for row in data_set[1:]: # we use [1:] to skip the header row.  
        year = row[3]
        row[7] = format_date(row[7], year)        # start_date
        row[8] = format_date(row[8], year)        # end_date
        row[9] = format_date_range(row[9], year)  # competition_date

    # Paris 2024 dates (hardcoded) we researched the dates of the paris 2024 olympics.
    for row in data_set[1:]: 
        if row[0] == "2024 Summer Olympics":
            row[7] = "26-Jul-2024"
            row[8] = "11-Aug-2024"
            row[9] = "26-Jul-2024 to 11-Aug-2024"

    write_csv_file("new_olympics_games.csv", data_set)

# Chloe kim
# This function reads the olympics_country file, format data, and store into dictionary. 
# data_set: The CSV data of olympics_country files 
# countries: This functions returns a dictionary of original country data. 
# Key = NOC 
# value = country name
def loadCountryDataAndFormatting(data_set):

    countries = {}

    for row in data_set[1:]:
        noc = row[0].strip().upper()
        country = row[1].strip()
        countries[noc] = country
    
    return countries

# Chloe Kim
# This function read the Paris/nocs file, format data, and store into dictionary
# data_set: The CSV data of paris nocs file.
# paris_nocs: This functions returns a dictionary of paris noc data.
# Key = paris Noc code
# value = country name
def loadParisDataAndFormatting(data_set):
    paris_nocs = {}

    for row in data_set[1:]:
        code = row[0].strip().upper()
        country = row[1].strip()
        paris_nocs[code] = country
    
    return paris_nocs

# Chloe Kim
# This function merges the Paris noc data and original olympic country dataset.
# It checks each Paris NOC code and adds it to the dictionary if it is not existed. 
# countries: A dictionary containing the original olympic country data
# paris_nocs: A dictionary containing Paris NOC data. 
# This function returns the updated countries dictionary after appending paris noc that is not in the file. 
def mergeOlympicsAndParis(countries, paris_nocs):
   
    for noc_code in paris_nocs:
 
        if noc_code not in countries:
            countries[noc_code] = paris_nocs[noc_code]
    
    return countries

# Chloe Kim
# This function converts the data stored in the dictionary into a list
# countries: A dictionary that has the completed noc data
# data_set: This function returns a list of noc data lists representing the CSV structure. 
# The header is noc and country. 
def convertDictToList(countries):
    data_set = [["noc", "country"]]

    for noc in countries:
        country = countries[noc]
        data_set.append([noc, country])

    return data_set

# Chloe Kim
# This function converts the data stored in the dictionary into a list
# athletes: A dictionary that has the completed athletes data
# data_set: This function returns a list of noc data lists representing the CSV structure. 
# The header is athlete_id, name, sex, born, height, weight, country, country_noc. 
def convertBioDictToList(athletes):
    data_set = [["athlete_id", "name", "sex", "born", "height", "weight", "country", "country_noc"]]

    for athlete_id in athletes:
        athlete = athletes[athlete_id]
        data_set.append([
            athlete["athlete_id"],
            athlete["name"],
            athlete["sex"],
            athlete["born"],
            athlete["height"],
            athlete["weight"],
            athlete["country"],
            athlete["country_noc"]
        ])

    return data_set

# Chloe kim
# This function does formatting athlete birth dates into the dd-Mon-yyyy format. 
# This function removes whitespace, handle missing values, converts a default date  01-Jan-yyyy format
# However, it supports the data formats listed in birth_formats, and uses a default estimate only for year values.
# date_birth_str: a birth date value that appears in different formats or missing
# It returns a formatted date string in the form dd-Mon-yyyy
def format_birth(date_birth_str):
    date_str = str(date_birth_str).strip()

    if date_str == "" or date_str == "-":
        return ""

    if len(date_str) == 4 and date_str.isdigit():
        return f"01-Jan-{date_str}"

    birth_formats = [
        "%d-%b-%y",
        "%d-%b-%Y",
        "%d %B %Y",
        "%d %B %y",
        "%Y-%m-%d",
    ]

    for fmt in birth_formats:
        try:
            dt = datetime.strptime(date_str, fmt)
           
            if "%y" in fmt and dt.year > datetime.now().year:
                dt = dt.replace(year=dt.year - 100)

            return dt.strftime("%d-%b-%Y")
        except ValueError:
            continue

    return ""

# Chloe Kim
# This function read the original olympics data file, format data, and store into dictionary
# data_set: The CSV data of original olympic athlete bio file.
# athletes: This functions returns a dictionary of athlete bio data.
# Key = athlete id
# value = formatted athlete information such as name, sex, born, height, weight, country, country_noc
# Assumes the olympics athlete dataset has the expected column positions.
def loadBioDataAndFormatting(data_set):
 
    athletes = {}

    for row in data_set[1:]:
        athlete_id = row[0]
        athletes[athlete_id] = {
        "athlete_id" : athlete_id,
        "name" : row[1].strip().title(),
        "sex" : row[2].strip().title(),
        "born" : format_birth(row[3]),
        "height" : row[4] if row[4] != "" else "",
        "weight" : row[5] if row[5] != "" else "" ,
        "country" : row[6].strip().title(),
        "country_noc" : row[7].strip().upper()
    }
    
    return athletes

# Chloe Kim
# This function read the Paris/athlete bio file, format data, and store into dictionary
# data_set: The CSV data of paris athlete bio file.
# paris_athletes: This functions returns a dictionary of paris athletes data.
# Key = paris athlete Id
# value = formatted athlete information such as name, sex, country_noc, country, height, weight, born
# Assumes the Paris athlete dataset has the expected column positions.
def loadParisBioDataAndFormatting(data_set):
    paris_athletes = {}

    for row in data_set[1:]:
       code = row[0]
       paris_athletes[code] = {
       "athlete_id" : code,
       "name" : row[2].strip().title(),
       "sex" : row[5].strip().title(),
       "country_noc" : row[7].strip().upper(),
       "country" : row[8].strip().title(),
       "height" : row[13] if row[13] != "" else "",
       "weight" : row[14] if row[14] != "" else "",
       "born" : format_birth(row[17])
       }
  
    return paris_athletes

# Chloe Kim
# This function merges the Paris athletes and original olympic athletes dataset.
# It checks each Paris athlete records and adds it to the dictionary if it is not existed. 
# athletes: A dictionary containing the original olympic athletes data
# paris_athletes: A dictionary containing Paris athletes data. 
# athletes: This function returns the updated athletes dictionary after appending paris athletes that is not in the file. 
def mergeBioDataSetAndParis(athletes, paris_athletes):

    for paris_bio_code in paris_athletes:
        paris_athlete = paris_athletes[paris_bio_code]

        if paris_bio_code not in athletes:
            athletes[paris_bio_code] = {
                "athlete_id" : paris_athlete["athlete_id"],
                "name" : paris_athlete["name"],
                "sex" : paris_athlete["sex"],
                "born" : paris_athlete["born"],
                "height" : paris_athlete["height"],
                "weight" : paris_athlete["weight"],
                "country" : paris_athlete["country"],
                "country_noc" : paris_athlete["country_noc"]
            }
    
    return athletes

# This main function is the function that the runner will call
# The function prototype cannot be changed
def main():

    # Chloe - bio
    # This section reads the original olympic athlete bio and paris athletes,
    # formats both datasets, and merges them and creates a new file
    athletes_data_set = read_csv_file("olympic_athlete_bio.csv")
    athletes = loadBioDataAndFormatting(athletes_data_set)
    
    paris_athletes_data_set = read_csv_file("paris/athletes.csv")
    paris_athletes = loadParisBioDataAndFormatting(paris_athletes_data_set)
    
    merged_bio_data = mergeBioDataSetAndParis(athletes, paris_athletes)
    converted_bio_data = convertBioDictToList(merged_bio_data)
    write_csv_file("new_olympic_athlete_bio.csv", converted_bio_data)

      
    # Chloe - bio
    # This section reads the original olympic countries and paris countries,
    # formats both datasets, and merges them and creates a new file
    athletes_data_set = read_csv_file("olympic_athlete_bio.csv")
    countries_data_set = read_csv_file("olympics_country.csv")
    countries = loadCountryDataAndFormatting(countries_data_set)

    paris_noc_data_set = read_csv_file("paris/nocs.csv")
    paris_countries = loadParisDataAndFormatting(paris_noc_data_set)
    merged_noc_data = mergeOlympicsAndParis(countries, paris_countries)
    converted_noc_data = convertDictToList(merged_noc_data)

    # Yuan Jie Wong - sort countries
    sorted_noc_data = sort_country(converted_noc_data[1:])
    converted_noc_data = [converted_noc_data[0]] + sorted_noc_data

    write_csv_file("new_olympics_country.csv", converted_noc_data)

     
    ## Erik - Clean and format olympics_games.csv
    create_olympics_games("olympics_games.csv") 

    ## Yuan Jie Wong - read athlete event results
    athlete_event_result_file = read_csv_file("olympic_athlete_event_results.csv")  
 
    ## Yuan Jie Wong - append new AGE FIELD at the end for olympic_athlete_event_results.csv
    append_col(athlete_event_result_file, "age")
    add_age(athlete_event_result_file, converted_bio_data)
 
    ## Yuan Jie Wong - add age column and append paris data to athlete event results
    paris_medallists = read_csv_file("paris/medallists.csv")
    athletes_dict, event_res_dict = append_paris_medallist_results(athlete_event_result_file, paris_medallists)

    # get paris athlete results and add it to the whole athlete event results file
    append_paris_athlete_results(athlete_event_result_file, paris_athletes_data_set, athletes_dict, event_res_dict)

    ## Yuan Jie Wong - create new athlete results file
    write_csv_file("new_olympic_athlete_event_results.csv", athlete_event_result_file)

    # Santiago - Insert summarized data overall to new_medal_tally.csv
    # This function also creates the corresponding file
    populate_medal_tally()