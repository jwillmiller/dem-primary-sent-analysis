# Twitter Sentiment Analysis to Predict the Democratic Primary
Final project for HOD 3200 - Introduction to Data Science at Vanderbilt University. Professor William R. Doyle.

I created this project using Python to collect and pre-process data and R to model and present it. The project was started in September 2019
and presented in December 2019. 

The scripts under the 'pi' directory were hosted on my Raspberry Pi and the 'demStreamer.py' script was run via a `cron` job twice weekly to
collect data. The data was then gathered from the Pi using `scp`, where it was processed in the 'HOD Data Science Pre-Processing.ipynb'
notebook. Here, the data was cleaned and put into spreadsheet form using `pandas`, and some sentiment analysis was also conducted. The 
notebook output was an Excel file, which was then read into `R`. The final report source code is the .Rmd file and the final report has been
knit into the .html file, which was the final deliverable for the project.
