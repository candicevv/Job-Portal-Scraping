# Job-Portal-Scraping
#### This is used for job opportunity scraping which may be used for future research.
##### Research may be updated in the future

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
