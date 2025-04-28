# Initial Design Thoughts

The design of this project is will be directed by trying to hit goals as layed out in the project readme. The design won't make much sense in terms to trying to do useful work.

The basic plan currently is to take free data from nasdaq.com and join it together to see trends. The 3 3rd party datasets I plan to join currently are home prices, ~bank data~, and ~agricultural data~. I plan to use data from bigquery ~about covid 19 to simulate in-house data~. I plan to normalize the data into median or mean averages, split by states in the USA. Then I plan to feed it into the core logic to calucate ratios and anything else that seems interesting, then order it by rank from best to worst along different sort fields.

Update: The other data sources had proplems such as only values for the entire US instead of by state, so now I have median home price from nasdaq.com and median hay price from bigquery.