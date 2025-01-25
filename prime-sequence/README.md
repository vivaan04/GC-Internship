# Working
Extracting google search results from selenium is very slow, prone to errors and challenging to scale. So I use [Google Custom Search JSON API](https://developers.google.com/custom-search/v1/overview).

I created a new custom search engine and API key. The search engine shows results only from amazon.in.

I use `curl` to send GET HTTP request with search query, search engine ID and API key. The GET request returns results in JSON form.

Then I extract the result links and I can optionally open them in chrome with Playwright.

The `search-api.sh` file is the main program. `open_select.py` is used to open the results in chrome. Two separate files contain the search engine ID and API key.



# Output
All output image/video are found in [this folder](https://drive.google.com/drive/folders/1M8Y_1PIXCRGlXSterdyXl-LLyqnK5IoT?usp=drive_link)

- [This video](https://drive.google.com/file/d/1V5oe3fYTxfndv9sGiJuMuCeYZzUVEkS7/view?usp=sharing) shows the running of full program
- [This image](https://drive.google.com/file/d/1xI1m4LUZL3VO-B_88--GmcRVPJCK1aum/view?usp=drive_link) demonstrates basic `curl` command.
- [This image](https://drive.google.com/file/d/1nOyTXTB0LTz5D47UzqWqTped9lhbUftf/view?usp=sharing) shows full program results
- [This image](https://drive.google.com/file/d/1cSbS6AvZfKVoMx7rA8cQBMeC1noy_N7u/view?usp=sharing) shows the custom search engine

