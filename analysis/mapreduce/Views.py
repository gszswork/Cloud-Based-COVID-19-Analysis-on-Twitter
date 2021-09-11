import couchdb
from couchdb.client import ViewResults

# The name of database can be switched to the expected one to add views.

server = couchdb.Server('http://admin:admin@172.26.133.210:5984/')
db = server['melbourne2016']

# In "covid_test" database
newdoc = {
  "_id": "_design/newdoc",
  "views": {
    "geo": {
      "map": "function (doc) {\n  if(doc.geo != 0 ){\n  emit(doc.geo, 1);\n  }\n}"
    },
    "datetext": {
      "reduce": "_stats",
      "map": "function (doc) {\n  emit([doc.date, doc.text], 1);\n}"
    }
  },
  "language": "javascript"
}

# In "melbourne2016" database
melbourne2016 = {
  "_id": "_design/melbourne2016",
  "views": {
    "rev": {
      "reduce": "function (keys, values, rereduce) { return sum(values);}",
      "map": "function (doc) {\n  emit(doc._rev, 1);\n}"
    },
    "date": {
      "reduce": "_stats",
      "map": "function (doc) {\n  emit(doc.date.split(\" \")[0],1);\n}"
    },
    "language": {
      "map": "function (doc) {\n  emit(doc.language , doc.geo);\n}"
    },
    "reducelanguage": {
      "reduce": "_stats",
      "map": "function (doc) {\n   emit(doc.language , 1);\n}"
    },
    "textdate": {
      "map": "function (doc) {\n  emit([doc.date, doc.text],1);\n}"
    }
  },
  "language": "javascript"
}

# in "melbourne20_21" database
melbourne20_21 = {
  "_id": "_design/melbourne20_21",
  "views": {
    "date": {
      "reduce": "_stats",
      "map": "function (doc) {\n  emit(doc.date.split(\" \")[0],1);\n}"
    },
    "textdate": {
      "map": "function (doc) {\n  emit([doc.Create_data, doc.text], 1);\n}"
    }
  },
  "language": "javascript"
}

# in "sentiment_analysis" database
sentiment_analysis = {
  "_id": "_design/sentiment_analysis",
  "views": {
    "sentiment": {
      "reduce": "_stats",
      "map": "function (doc) {\n  emit(doc._id.split('/'), doc.sentiment_score);\n}"
    }
  },
  "language": "javascript"
}

# in "sentiment_covid" database
sentiment_covid = {
  "_id": "_design/sentiment_covid",
  "views": {
    "sentiment": {
      "reduce": "_stats",
      "map": "function (doc) {\n  emit(doc._id.split('/'), doc.sentiment_score);\n}"
    }
  },
  "language": "javascript"
}

# in "sentiment_location" database
sentiment_location = {
  "_id": "_design/sentiment_location",
  "views": {
    "sentiment": {
      "map": "function (doc) {\n  emit([doc.text,doc.sentiment_score], doc.lga);\n}"
    }
  },
  "language": "javascript"
}

# in "sentiment_location_lga" database 
sentiment_location_lga = {
  "_id": "_design/dsentiment_location_lga",
  "views": {
    "sentiment": {
      "map": "function (doc) {\n  emit([doc.text,doc.sentiment_score], doc.lga)\n}"
    }
  },
  "language": "javascript"
}
