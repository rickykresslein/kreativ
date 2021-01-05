# Kreativ
Kreativ edits and tracks your creative hours.

## More info...
After listening to an interview with [Jim Collins on The Tim Ferris Show](https://tim.blog/2019/02/18/jim-collins/) podcast, I started tracking the hours I spent doing creative activities every day. In the interview, Jim says your past 365 days should always be over 1,000 hours. You can use the past 90 and 180 days as a marker to help keep you on track for this goal. I'm not great with spreadsheets, so I wanted a program that would track these hours for me. I created Kreativ, and with it you can add or change hours to new or existing days and easily calculate how many hours are in the best day, month, 90 days, 180 days, year, or any given year.

## Getting Started
You can download the binaries for Linux, Windows, and Mac on my website, [https://kressle.in/kreativ](https://kressle.in/projects/kreativ), or you can download the source here to compile it yourself.

## Use
The program allows you to set a date and input a number of hours. When you click submit, those hours will be stored together with the date in a CSV file. The default location of the file is ~/Documents/Kreativ/creative_hours.csv. You can edit this file using a spreadsheet editor, or through Kreativ alone.

If you enter hours for a date that already exists, Kreativ will ask if you wish to replace the hours for that date or add to them. There is no way to remove hours for a selected date at this time, besides opening the CSV file in a spreadsheet editor and doing it manually, or by setting the date to 0 creative hours through Kreativ.

The bottom section of the app is for tracking stored hours. There you can see how many creative hours you had today, yesterday, in the past 30, 90, or 180 days, in the past year, or in a selected year.

## Project Details

### Built With
Kreativ was built on 100% Python using PyQt5.

### License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE.md](LICENSE.md) file for details.

### Author
This project is created and maintained by [Ricky Kresslein](httsp://kressle.in). 

### Acknowledgements
Thank you to [Jim Collins](https://www.jimcollins.com/) and [Tim Ferriss](https://tim.blog) for the great podcast interview that provided the inspiration for this project.
