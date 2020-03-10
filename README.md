# Project Mine
## Getting Started with the App and CSV Generator
Using the App...
1. Open the app which you use to access the command-line
2. Navigate to directory containing celitech/celitech/app.py, you should be in the second celitech directory
3. Using the command-line, run the following: python app.py
4. Copy and paste the listed IP into your browser of choice, note that this is localhost - the url will not be available to others over the internet
Using the CSV Generator
1. Starting from Step 2 above, use the command-line to run the following: create_aggregate_user_csv.py "dd-mmm-yy" "dd-mmm-yy"
Date examples: 1-Jul-19, 22-Sep-20
Note: the first date corresponds to the start of the period and the second to the end.
## Features
1744 .csv files, containing 1+ sessions (rows) with following info...
1. ICCID: a general ID parameter
2. CONNECT_TIME: when a session is started
3. CLOSE_TIME: when a session is finished
4. DURATION: shows how much cellular data (in bytes) is consumed during the session
5. COUNTRY_NAME: country where the session is consumed
## Scope
1. Find better/more optimal approach/tool within AWS environment, or outside it
2. Better organize & visualize data in aggregate (monthly) and by ICCID
3. New meaningful patterns/insights over time
## Deliverables
### Visualizations
#### csv_combiner.py
This script is for your personal use to combine several csv files exported by AWS to one file. To use, port all desired csv files to one folder, and reference the correct directory in line _ of the script.
#### simple_bar_graph.py
![](https://github.com/marygooneratne/celitech/blob/master/visualizations/simple.png)
This python script parses the data from July-August 2019 to generate the graph above, a visualization of data usage (in MB) by user.
#### racing_bar_graph.py
This python script parses the data from July-August 2019 to generate the graph above, a visualization of data usage (in MB) by country. The visualization is animated, showing the increase in usage for each country over time. The number on the right shows the day, beginning in June. The file is available as visualizations/racing_bar_graph.gif.
#### global_heat_map.py
![](https://github.com/marygooneratne/celitech/blob/master/visualizations/heatmap.png)
This python script parses the data from July-August 2019 to generate the graph above, a global heatmap illustrating countries’ respective usages. This visualization is interactive when run locally.
#### duration_scatter.py
![](https://github.com/marygooneratne/celitech/blob/master/visualizations/scatter.png)
This python script parses the data from July-August 2019 to generate the graph above, a visualization comparing the length of a connection to how much data it used.
### QuickSight Analysis
#### What is QuickSight?
Tool that allows you to connect data sources, analyze and apply ML to data, builds dashboards, and then embed dashboards or receive email reports
#### Features
* AWS integration with RedShift, S#, Athena, Aurora, RDS, IAM, CloudTrail, Cloud Directory
* Uses SPICE: designed for fast, ad hoc data visualization
* Platform includes Analyses (workspace), Visuals (graphs, charts, etc.), Insights (ML insights, interpretations), Sheets (groups of visuals, groups of sheets in an alalysis), and Stories (slideshows of visuals)
* Pay-per-session
#### Pros/Cons
##### Pros
1. Easy onboarding
2. Data integration
3. Cost friendly
4. Visaulization recommendations
##### Cons
1. No android support
2. Not a lot of graph/chart options, not very customizable (no maps, plain tables)
3. Not a lot of functionality
4. Not as secure as Power BI
#### Similar Tools on Market
* Tableau
* QlickView
* SAS
* IBM Cognos
* Google Data Studio
* Power BI
