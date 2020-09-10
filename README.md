# knn_price
This is a personal project where I am looking to efficiently check pricing of products given any webpage.
It's pretty simple to create a web extractor for a particular page, or even pages within the same domain. However, there is no standard websites conform to, so it's unlikely an extractor for one domain would work on another domain (different layouts, selectors, naming conventions and sometimes even technologies).

# Basic Idea
I use Selenium to navigate to web pages. The benefit of using Selenium is that it loads the webpage in browser, as it was meant to be seen, and also offers usefule tools for traversal.

Javascript is injected once the page loads which extracts visible data (i.e. the important information like Title and Price; leaving out reviews, comments or product recommendations. This extract is (for sake of ease) stored in/read from a SQLite database using peewee DBM.

The data is loaded into a pandas dataframe where it's original values can be preprocessed before being converted to a numpy dataset and fed into DBSCAN for clustering. I've implemented a labeller using partially labelled data. By labelling all of the datapoints for Title, we can determine the minimum epsilon required to cluster all Titles together, as well as the max (the maximum epsilon value before a non-labelled datapoint gets included in the Title cluster), with increment passed in as a parameter.

# Next steps

By taking the mid way (or better yet, a todo; using multiple labelled datasets) of those points, you can label the other clusters, setting those labels in the database. Once all of the data has been labelled, we can train model (planning on using k-nearest neighbour and the same features used during clustering) to build a generalised model.

Following that: include further domains to build an even better model, and have the model detect "sale price"

# Great sources of info:
"Web Content Extraction Through Machine Learning", Ziyan Zhou & Muntasir Mashuq
"Sociopath: Automatic Local Events Extractor", Galina Alperovich
