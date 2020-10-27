# knn_price
Personal project.
The idea is to train a knn model which will classify text from a given "product page" into classes like Product Title, Price, Sale Price, Rating, for a number of *different domains*.
Extractors for 1 domain is easy enough to build but won't work on any other site. I hope to build a generalised model that can do that for any product page from any given domain.

# Basic Idea
crawler -> navigate to url, extract data -> push data to db
db -> dataframe + cluster labels -> feature processing -> pre-processing -> clusterer + get labels -> derived labels to db
derived labels -> knn model

## Cluster labels & derived labels
Cluster labels are manually labelled. These labels are used to calc min/max epsilon values for each cluster. By manually labelling classes that appear once per page ("Page Title", "Price", "Sale Price"), and which should form a unique cluster, we can calculate a "best fit" eps value between the smallest min and smallest max derived from labelled clusters. Using this "main" model, we can produce labels for all clusters.

## Features
Want to 0/1 the outcomes of feature functions so that datapoints as separated as possible
Distinguishing Price and Sale Price
- strike-through
- text-colour
- font-size
Text Colour
- is_it_coloured() function
Denomination
- text breakdown / character counts

## Clustering

# Tests:
`python -m unittest test.tests`

# Sources of info:
"Web Content Extraction Through Machine Learning", Ziyan Zhou & Muntasir Mashuq
"Sociopath: Automatic Local Events Extractor", Galina Alperovich
