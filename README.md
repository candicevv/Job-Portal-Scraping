# Job-Portal-Scraping
#### This is used for job opportunity scraping which may be used for future research.
##### Research may be updated in the future

## Problem Face:
- [x] **Date Selection**

Select specific date and page that is need to scrape.

- [ ] **Google connection and update**

Updating to Google may meet problem of write in limit. In order to prevent this problem, need to add in `sleep`. However, and request is so large (usually 80 pages * 20 request per day, and weekly updated), even a 1 second sleep is very time consuming.
Unsure would there be any other solution to avoid write in limit for Googlesheet.

- [ ] **Selenium break when internet not good enough**

Refer to [Stackoverflow Question](https://stackoverflow.com/questions/4766556/repeat-python-function-call-on-exception), when Internet is not good enough, can try picking up objects for several times until the page is successfully loaded.
```
import functools
def try_5_times(fn):
    @functools.wraps(fn) #keeps name and docstring of old function
    def new_fn(*args, **kwargs):
        for i in range(5):
            try:
                return fn(*args, **kwargs)
            except:
                time.sleep(1)
                pass
    return new_fn
```
Can solve the problem sometimes, but still may face error.
May need other solution.


## Steps of whole process:
### Set up API for code update
**Set up Googlesheet API through Google**

Download API key from Google and saved as `secret.json` for connection. Set up API service through the following code.
```
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('secret.json', scope)
```
Connect to the Googlesheet that is needed to update.
```
gc = gspread.authorize(credentials)
wks = gc.open("Career").sheet1
```
As all the update is adding under the existing rows, we need to first know how many rows we have. In this case, the first step of the scraping is to restructure the sheet we have. First column of the sheet is the **date of publishment**, which is a non-null cell in this sheet, in this case, it can be used as length count.
```
n_row=len(wks.col_values(1))
```
