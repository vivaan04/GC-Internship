GetSearchResults Class:
This class is designed to retrieve search results from Google based on a given query and extract relevant information such as titles, descriptions, and URLs from the search results.

Functions:
__init__(self, search_query: str, n_scrolls: int = 2) -> None:

Aim: Initializes the class and sets up a Chrome WebDriver.
Parameters:
search_query: The search query to look up on Google.
n_scrolls: Number of times to scroll down the search results page to load more content (default is 2).
Process:
Opens a Chrome browser and navigates to Google's search results page for the provided query.
Scrolls through the page to load additional search results according to the specified scroll count.
Calls the _extract_info() method to extract relevant data.
_scroll_page(self):

Aim: Simulates scrolling down the web page to load more search results.
Process:
Locates the <body> element of the page and sends an 'END' key press event to simulate scrolling.
Waits for a short duration (2 seconds) to allow the content to load.
_extract_info(self):

Aim: Extracts titles, descriptions, and URLs from the loaded search results.
Process:
Finds and extracts relevant information such as titles, descriptions, and URLs from the loaded search results.
Stores the extracted data in respective lists.
to_csv(self, file_path):

Aim: Saves the extracted search results into a CSV file.
Parameters:
file_path: The path where the CSV file will be saved.
Process:
Creates a Pandas DataFrame from the extracted data.
Writes the DataFrame to a CSV file at the specified file path.