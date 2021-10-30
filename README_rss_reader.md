#Python RSS-Reader
Pure Python command-line RSS reader.

##Installation
###Dependencies
* requests >= 2.26
* bs4 >= 4.10.0
* lxml >= 4.6.3
* xhtml2pdf >= 0.2.5

###User installation
The easiest way to install rss_reader is using pip and tar.gz file

##JSON
Below is the JSON structure that is used when printing JSON in stdout and caching news.

[

    {
        "date": "2021-10-26T20:03:35Z",
        "title": "North Dakota man",
        "source": "Associated Press",
        "category": null,
        "link": "https://news.yahoo.com/north-dakota1.html",
        "enclosure": "E:\\DEV\\92e2fc5f45.jpeg",
        "description": null,
        "links": [
            "https://news.yahoo.com/north-dakota.html",
            "http://www.ap.org/",
            "https://s.yimg.com/uu/api/res/"
        ]
    },
    {
        "date": "2021-10-26T19:50:00Z",
        "title": "Students suspended",
        "source": "Tahlequah Daily Press, Okla.",
        "category": null,
        "link": "https://news.yahoo.com/students.html",
        "enclosure": null,
        "description": null,
        "links": [
            "https://news.yahoo.com/.html",
            "https://www.tahlequahdailypress.com"
        ]
    },
    {
        "date": "2021-10-26T18:36:55Z",
        "title": "Lawsuit: Suburban St. Louis",
        "source": "Associated Press",
        "category": null,
        "link": "https://news.yahoo.com/lawsuit.html",
        "enclosure": "E:\\DEV\\.jpeg",
        "description": null,
        "links": [
            "https://news.yahoo.com/lawsuit.html",
            "http://www.ap.org/",
            "https://s.yimg.com/uu/api/res/"
        ]
    }
]