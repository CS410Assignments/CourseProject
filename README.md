# Lecture Search and Slide Segmentation



## Introduction

### Problem Statement & Motivation 

Online learning platforms and MOOCs such as Coursera have democratized education and enabled millions of students to access knowledge at a previously unthinkable scale. These platforms host thousands of hours of extremely rich content that not only expose their audiences to valuable concepts and ideas, but also serve as crucial reference materials after the content has been initially viewed (for example, while studying for an exam or upon attempting to implement a learned concept in the real world).

However, in their current state, most MOOCs are not fully mature platforms and do not provide users with effective tools to quickly find and access specific content. In general, revisiting a target topic requires considerable effort on the part of the user and often involves clicking through multiple (potentially) relevant lectures and exhaustively scrubbing through videos to access the concept of interest.

[SmartMOOCs](https://smartmoocs.web.illinois.edu/) is an experimental MOOC platform created at UIUC that serves as a motivating example by demonstrating how advanced features can augment existing technology and enhance the student experience. At present, the lectures on [SmartMOOCs](https://smartmoocs.web.illinois.edu/) are uniformly partitioned into one-minute segments acting as proto-topics, which does not accurately represent topics. A more effective approach could be to segment lectures based on the slides in a slideshow - one slide per topic. This approach benefits from using the same paradigm of information segmentation used in creating the slideshows, where each slide typically contains one key idea. A topic found based on the transcript or slide text would thus have a likely logical beginning and end, which creates new opportunities for presenting results to a user, for example as a playlist.

### Proposed Solution

The goal of this project is to implement enhancements to an intelligent learning platform (much like, [SmartMOOCs)](https://smartmoocs.web.illinois.edu/) and demonstrate that a more intuitive and efficient learning experience is acheivable. In particular, this project aims to:

1) incorporate keyword and query search functionality (primary objective), and
2) identify better ways to segment lectures based on topic transitions (stretch goal).



## Usage

### Using the Deployed (Live) Web Application

The web app has been populated with Coursera content (slides, videos, and transcripts) for CS 410: Text Information Systems and can be accessed [here](https://stingray-app-3sdu7.ondigitalocean.app/).

![Screenshot 2022-12-05 at 9.46.30 AM](https://user-images.githubusercontent.com/45109940/205754860-f3dce1b6-433d-472e-87fb-9008a3737059.png)

Using the app to search CS 410 course content is intuitive and straightforward - simply specify whether you want the application to:

- search across "Lectures" (entire lessons) or among individual "Slides", and 
- how many search results you would like the application to return (between 5 and 10, inclusive)

The application then returns links to relevant course content based on the user's query specifications and provides a brief excerpt/summary for each result extracted from the applicable lecture transcript.

![Screenshot 2022-12-05 at 9.59.03 AM](https://user-images.githubusercontent.com/45109940/205754758-cabf9c3c-4091-461f-890d-953a592a8b54.png)

Upon selecting one of the links provided, an embedded video player appears and begins playing the applicable content:

- If the *"Search Lectures"* option was selected, the video will start playing from the beginning of the lecture. 
- If the *"Search Slides"* option was selected, the application will automatically skip to the appropriate timestamp within the lecture video and begin there (since the returned results are more specific).

![Screenshot 2022-12-05 at 9.59.30 AM](https://user-images.githubusercontent.com/45109940/205754604-1389385d-04f8-41b2-94b6-c2469e2ac850.png)



In addition to retrieving and displaying the desired/queried content, the application also allows the user to download the video in MP4 format, a PDF of the applicable slides, or the text transcription for each of the associated results. Users also have the ability to advance forward and backward among the returned results using the "previous" and "next" buttons below the video player.

### Running the Application Locally

#### Prerequisites

- MacOS or Linux recommended (not tested on Windows)
- [nodejs 16+](https://nodejs.org/en/download/package-manager/)
- [yarn](https://classic.yarnpkg.com/en/docs/install)
- python 3.5.6 
  - We've found the most reliable way of installing python 3.5.6 and all of the python dependencies is by using [conda](https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html).

#### API

The API is the server-side component that handles HTTP requests from the Client application. This should be started in a terminal and left running before starting the Client application.

```sh
cd code/api
# create a conda environment with all python dependencies
conda env create -f environment.yml
# activate it
conda activate lecture_search
# run the database migrations
python manage.py migrate
# run the tests
python manage.py test
# run the api
gunicorn api.wsgi
```

This will start an HTTP server that serves requests at the following URL: http://localhost:8000/documents

Example request: http://localhost:8000/documents?search=paradigmatic%20relationship&corpus=cs-410&max_results=5

**Add instructions for shutting down port 8000 if already in use?**

#### CLI (Command Line Interface)

Alternatively, you may also try running the API directly from the command line:

```sh
# try searching from the command line (optional)
python lecture_search_cli.py
```

Running the command above will prompt the user for three parameters for each request:

1. Search query 
2. The corpus type (either "lectures" for lecture-level results or "cs-410" for slide-level results; default = 'lectures')
3. Number of results to return (default = 5)

<img width="558" alt="image" src="https://user-images.githubusercontent.com/94029406/205476050-c894e533-627b-4e25-9123-75d0d9a40fcf.png">


#### Client

The Client is a browser-based graphical user interface that issues HTTP requests to the API and displays user-friendly responses. These commands must be run in a separate terminal instance from the API, and left running while testing the application.

```sh
cd code/client
# install the dependencies
yarn install
# run the application
yarn start
```

The Client is available at the following URL: https://localhost:3000



## Implementation Details

- The Lecture Search Engine was created with the [metapy](https://github.com/meta-toolkit/metapy) NLP toolkit. 
- The Lecture Search Client was created with the [React](https://reactjs.org/) web application framework.
- The Lecture Search API was created with the [Django](https://www.djangoproject.com/) web application framework.
- All files including video, lecture text and slides are hosted on an [AWS S3](https://aws.amazon.com/pm/serv-s3/) bucket.

The API and Client are automatically deployed to the Digital Ocean platform every time a commit is pushed to the main branch.

The API only includes one endpoint: `/documents`. This endpoint accepts HTTP GET requests with a search query parameter. The search parameter is a space-separated list of words. The endpoint responds with a JSON formatted list of search results.

The live API can be accessed [here](https://sea-turtle-app-7y54u.ondigitalocean.app/documents/).

**ADD MORE EXPLANATION OF API USAGE**

Example: **(something other than "test"?)**

```sh
(base) ➜  api git:(main) curl https://sea-turtle-app-7y54u.ondigitalocean.app/documents/\?search\=test
{"corpus": "CS410_lectures", "query": "test", "results": [{"03_video_id": "W03_L06", "04_title": "Evaluation Of Tr Systems Practical Issues", "01_doc_id": 17, "06_txt_path": "path/to/W03_L06.txt", "02_score": 14.651, "05_vid_path": "path/to/W03_L06.mp4", "00_rank": 1}, {"03_video_id": "W03_L01", "04_title": "Evaluation Of Tr Systems", "01_doc_id": 12, "06_txt_path": "path/to/W03_L01.txt", "02_score": 11.206, "05_vid_path": "path/to/W03_L01.mp4", "00_rank": 2}, {"03_video_id": "W11_L02", "04_title": "Text Categorization Evaluation Part 1", "01_doc_id": 81, "06_txt_path": "path/to/W11_L02.txt", "02_score": 7.386, "05_vid_path": "path/to/W11_L02.mp4", "00_rank": 3}, {"03_video_id": "W12_L04", "04_title": "Contextual Text Mining Mining Causal Topics With Time Series Supervision", "01_doc_id": 89, "06_txt_path": "path/to/W12_L04.txt", "02_score": 4.599, "05_vid_path": "path/to/W12_L04.mp4", "00_rank": 4}, {"03_video_id": "W10_L06", "04_title": "Text Clustering Evaluation", "01_doc_id": 77, "06_txt_path": "path/to/W10_L06.txt", "02_score": 4.599, "05_vid_path": "path/to/W10_L06.mp4", "00_rank": 5}]}
```

### Architecture Diagram (Deployed)

```mermaid
C4Deployment
    title Component diagram for Lecture Search and Segmentation
    Deployment_Node(do, "Digital Ocean") {
        Deployment_Node(static_app, "Static") {
            Container(spa, "Single Page Application", "JavaScript and React " "Front end search application.")
        }
        Deployment_Node(dynamic_app, "Dynamic") {
            Container_Boundary(api, "Python and Django API", "") {
                Component(docs, "Documents Controller", "Controller", "Handles API requests for searching documents")
                Component(search_engine, "MetaPy Search Engine", "metapy", "Provides access to the inverted index to search for relevant documents")
                Rel(docs, search_engine, "Uses")
            }
        }
    }

    Rel_Back(spa, docs, "Uses", "JSON")
```

### Corpus creation

```sh
cd code/prep
# create a conda environment
conda create --name corpus_create python=3.9.15
# activate it
conda activate corpus_create
# install the dependencies
pip install -r requirements.txt
# download course using coursera-dl
coursera-dl -ca {your CAUTH cookie value} cs-410
# create corpus
python prep.py
```

Each directory in `code/prep` will result in a new corpus. The corpus creator was modeled on file names downloaded by [`coursera-dl`](https://github.com/coursera-dl/coursera-dl) for the `cs-410` course and may not work on others.

In principle, the same approach/implementation described above can be applied to any other course content derived from Coursera using [`coursera-dl`](https://github.com/coursera-dl/coursera-dl), although this has not yet been formally/rigorously tested and minor modifications may be required. 



## References

**The following resources were used when implementing the project:**

1. https://meta-toolkit.org/
2. https://github.com/meta-toolkit/metapy
3. https://github.com/coursera-dl/coursera-dl
4. https://www.djangoproject.com/
5. https://reactjs.org/
6. https://www.digitalocean.com/
7. https://spacy.io/usage
8. https://www.activestate.com/blog/how-to-do-text-summarization-with-python/
9. https://pypi.org/project/bert-extractive-summarizer/
10. https://pypi.org/project/transformers/
11. https://en.wikipedia.org/wiki/Natural_language_processing



## Contributors

### UIUC CS 410 - Fall 2022 | Team Early Birds* 

**Anthony Ghabour (Team Captain)**

- Lecture-level corpus, metadata, and ranking function development

 - Documentation and 

**Tina Tang**

- Ranking function testing and corpus validation 
- Documentation and instructional video development

**Rick Suggs**

- Client deployment
- Integration, deployment, and testing

**Maciej Wieczorek**

- Original concept
- Slide-level corpus and metadata development

**Quan Nguyen**

- Front-end development and content hosting
- Integration, deployment, and testing

\* Team members contributed equally and are listed in no particular order. 
