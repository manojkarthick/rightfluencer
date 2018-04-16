### RightFluencer

This repository contains the codebase and the documentation related to the CMPT 733 Project.

#### Web URL
The application is hosted on the Google Cloud platform at the following URL: [rightfluencer.ml](http://rightfluencer.ml)

#### What is RightFluencer ?

An interactive web application and dashboard that allows you to find the right influencers for your brand by analyzing their posts, images and videos.

#### Key Differentiators

* Collective analysis of multiple social media platforms in the same place using both metrics and content.
* Inspection of images to understand what products influencers are interested in to find their niche.
* Analyzing YouTube videos of influencers using the closed captions to better interpret their expertise.
* Influencer score based on both product and category.

#### Technology Stack

* Cloud Hosting: Google Cloud platform
* Visualization: Plotly, D3.js, matplotlib, pyLDAvis
* Web and UI: Apache web server, Flask, Bootstrap, Semantic UI, jinja2
* Data analysis: NLTK, KerasR, gensim, Pandas, Apache Spark, nGram, WordNet, PyMongo, Watson Personality Insights API
* Data cleaning: Pandas, Spark Dataframes
* Data storage: MongoDB
* Data collection: RESTful API Client, Web scrapers
* Data sources: Instagram, Facebook, YouTube, Twitter, Klout

#### Deploying the Application

* The application has been hosted on Google Cloud at [rightfluencer.ml](rightfluencer.ml)
* If you wish to run the application locally: Clone the repository and run the following commands.
``` cd web-app/
python3 app.py ```
* Dependencies to be installed: `flask`, `pymongo`, `plotly`, `requests`, `numpy`, `pandas`. These dependencies can be installed using `pip3` or `conda`
* The application has been tested with python3 using the anaconda python distribution.
* The database has to restored using the data available in the `mongo-data` folder. The name of the database is `influencers_db`.
* To install mongoDB on Mac OSX (.tar.gz install recommended) - [https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
* To install mongoDB on Ubuntu 16.04 - [https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)
* MongoDB port: 27017
* MongoDB server start/stop: `sudo service mongod start/stop` (Ubuntu) or `sudo mongod` (Mac)
* Start using Mongo through console: `mongo --host 127.0.0.1:27017`

#### Repository Contents

Some of the important components of RightFluencer are listed below:

* The repository has been organized based on the steps in the data science pipeline
* The actual web application is contained in the `web-app` folder.
* Data collection: `data-collection\<data_source.ipynb`
* Data aggregation: `data-aggregation\Aggregator.ipynb`
* Data cleaning: `data-preprocessing\Preprocess-NLP.ipynb`, `data-preprocessing\youtube-clean.ipynb`
* LDA: `data-analysis\LDA\`
* LSI: `data-analysis\TF-IDF\`
* nGram: `data-analysis\ngram\`
* Keras: `data-analysis\KerasModelsNotebook.Rmd`
* Flask app: `web-app\app.py`
* Visualization: `web-app\plots.py`