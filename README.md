#  ExpertSearch v2.0

## Abstract

The existing ExpertSearch system (https://github.com/CS410Assignments/ExpertSearch) has several features such as faculty search, filtering based search, search results (with options to open faculty bio pages, emailing, location info), pagination etc.
As a team, we did a deep analysis of the current ExpertSearch capabilities and found several deficiencies that need to be addressed to make it a better search system. 
The deficiencies include lack of accuracy, lack of relevant search results and inconsistencies in the search results. These deficiencies can be addressed using the right text retrieval and text mining techniques that will improve the overall search experience in the ExpertSearch system. 
The team involved in implementing features such as converting unstructured dataset to structured dataset (e.g., csv, json), identifying the key topics (e.g., areas of interest) for each of the faculties and display in the search result, introducing an admin interface that would classify faculty pages and finally improving some of the existing features in the search page for better search experience.

## Hardware Requirements
1. Modern Operating System  [Minimum]\
Linux or MacOS  **[Recommended]**

2. x86 64-bit CPU  [Minimum] \
x86 64-bit CPU Multi Core **[Recommended]** 

3. 8 GB RAM  [Minimum]\
16 GB RAM  **[Recommended]**

4. 5 GB free disk space

## Software Requirements

1. Chrome Browser, Version 96+ and above
   * [Download and Install Chrome](https://www.google.com/chrome/)
 
2. Python3.9 virtual environment
   * [MacOS Conda Installation Guide](https://www.anaconda.com/products/individual) or [Linux Conda Installation Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html)
   * [Managing Conda - Install python virtual environment using Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) 
   
   Run the below command in virtual environment and Make sure you have installed Python3.9.X.
   ```shell script
   python --version
   ````
      
3. `pip` package installed in python3.9 virtual environment  - _Should be default wiith Python3.9_   
   * To install pip on your virtual environment run below command
   ```shell script
   conda install pip 
    ````
4. git cli tool
    * [Install git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)   


## Setup

1. Set Environemnt Variable\
   [Click Here](https://cmt3.research.microsoft.com/CS410Expo2021/Submission/Summary/56) to get the Google API Key from the [CMT](https://cmt3.research.microsoft.com/CS410Expo2021/Submission/Summary/56) Abstract section (Make sure you are in reviewer role. Credentials required). \
    Add the below line in your `~/.basrc` or `~/.bash_profile` 
    ```shell script
    export GOOGLE_API_KEY=<Add Google api Key from CMT Abstract section>
    ```
    If using PyCharm, Pycharm Menu --> Preferences --> Build, Execution, Deployment --> Python Console --> Environment Variables: --> Add `GOOGLE_API_KEY=<Add Google api Key from CMT Abstract section>` --> Ok  

2. Using git clone the repository to a path
   ```shell script
   cd <desired path where you want to download the project>
   git clone https://github.com/sudiptobilu/CourseProject.git
   cd CourseProject
   ```
3. Switch to the Python3.9 virtual environemnt\
   If using Conda,
   ```shell script
   # TIP: Show all conda environemt
   conda env list   
   
   # pick the Python3.9 environment name from the above output. Then run
   conda activate <python3.9 virtual environment name> 
   ```

4. Install the project requirements file on Python3.9 virtual environment
    ```shell script
    pip install -r requirements.txt
    ```

## Usage
1. From the project directory and python3.9 virtual environment, Run the below command 
    ```shell script
   cd apps/frontend
   
    python server.py
    ````
2. Open Chrome browser and browse the below url
    ```shell script
   http://localhost:8095
    ````
3. The browser should show up ExpertSearchv2.0 search application 


## Workflows 

![alt text](docs/workflows/images/search.jpg?raw=true)
<br/>
<br/>
<br/>

![alt text](docs/workflows/images/admin.jpg?raw=true)


## Project Team Members

Name             |  Netid 
| :---  | :--- 
Ujjal Saha       | ujjals2
Arnab KarSarkar       | arnabk2
Sudipto Sarkar       | sudipto2





## User Stories and Team Assignments

1. **Epic: Crawling and Scraping**
    - - - -
    a. **User Story**: Crawler Implementation for a given webpage url
     
    In the admin interface when admin inputs an url, this story takes the url as input and scrapes the page and extracts the faculty biodata. We also implemented intelligent logic in scraper to find right faculty page if the base url has links that leads to multiple faculty related pages. 

    **Executed by**: _Arnab KarSarkar, Ujjal Saha_
    - - - -
    b. **User Story**: Adding admin interface for web page indexing  
    
    As our project scope doesn’t include auto crawler features for the entire web, the admin interface we are implementing in ExpertSearch system is to allow the admin to enter base url of the universities and based on valid/invalid university email (different story) the admin interface will fetch the url to the crawler module to scrape faculty data.
    
    **Executed by**: _Arnab KarSarkar, Ujjal Saha_
    - - - -
    c. **User Story**: Displaying accepted/rejected web page based on url   
    
    When admin enters the base url, this module will check if the url is a valid university url. If yes, the module forwards the url for crawling and scraping the faculty pages. If not, the module lets the admin know that base url doesn’t belong to a university or no faculty page found.
                     
    **Executed by**: _Arnab KarSarkar, Sudipto Sarkar_
    - - - -

2. **Epic: Search Experience Enhancement**   

    a. **User Story**: Build a structured dataset from Unstructured datasets 

    In current ExpertSearch system the faculty data are stored as unstructured data as a file. We are implementing a functionality that will convert the unstructured data to structured data. For e.g., using text mining and text retrieval techniques we are planning to extract fields like Faculty Name, Department, University, Area of Interests, email, phone, etc, and store them in a structured form (either in csv, or database etc.) This will enhance the overall search experience. 
    
    **Executed by**: _Ujjal Saha, Sudipto Sarkar_
    - - - -
    b. **User Story**: Enhance the search experience with relevant search results  
    
    Based on search input, we will look up all biodata from structured dataset and implement a ranking function using metapy. Based on ranking results we will extract corresponding fields from the structured data and display as search results. We will enhance filter based searching feature too where user can get better accuracy because of structured dataset.
    
    **Executed by**: _Ujjal Saha, Sudipto Sarkar_
    - - - -
    c. **User Story**: Better consistency in displaying links such as email, phone etc. leveraging the structured data   
    
    The current expert search system doesn’t show contact info (email, etc.) consistently across the search results even if the faulty page does have the data. Our improved scraping and structured data along with improved data display logic will increase the consistency in displaying the fields in search results.                 
    
    **Executed by**: _Ujjal Saha, Sudipto Sarkar_
    - - - -
    
3. **Epic: Topic Mining**   

    a. **User Story**: Using text mining techniques to extract the Areas of interest for a given faculty based 

    Using text mining methods we are planning to generate “Areas of Interests” data from the faculty bio. We are using guided LDA algorithm and Gensim/NLTK libraries to explore other topic mining features and we will be experimenting with parameters to generate relevant topics. 
    
    **Executed by**: _Sudipto Sarkar, Arnab KarSarkar_
    - - - -
    b. **User Story**: Display Areas of Interest in the faculty search result  
    
    We are enhancing the front end of ExpertSearch to display faculty search results along with additional relevant fields such as faculty areas of interest and few more.
    
    **Executed by**: _Sudipto Sarkar, Arnab KarSarkar_
    - - - -
    
4. **Epic: Deployment**   

    a. **User Story**: Understand and Install current ExpertSearch System 

    Install and explore the ExpertSearch system and understand the features and functionalities (both frontend and backend). Experiment with code changes etc.  
    
    **Executed by**: _Ujjal Saha, Sudipto Sarkar, Arnab KarSarkar_
    - - - -
    b. **User Story**: Deploy code into AWS  
    
    As ExpertSearch is web-based framework, we will do our deployments in AWS Cloud and make it public. We will also do a git PR on the existing original ExpertSearch repo. But launching as an improved system and others to validate, we will separately host ExpertSearchv2.0 in Heroku. 
    
    **Executed by**: _Arnab KarSarkar, Ujjal Saha, Sudipto Sarkar_
    - - - -
    c. **User Story**: Validation Exercises  
    
    As we do development and deployment, we are doing multiple rounds of verification and validation and some will require integrated end-to-end validation steps.  
    
    **Executed by**: _Sudipto Sarkar, Arnab KarSarkar, Ujjal Saha, _
    - - - -
    
5. **Epic: Documentation**   

    a. **User Story**: Proposal Documentation 
    
    **Executed by**: _Ujjal Saha, Sudipto Sarkar, Arnab KarSarkar_
    - - - -
    b. **User Story**: project Progress Documentation
    
    **Executed by**: _Arnab KarSarkar, Ujjal Saha, Sudipto Sarkar_
    - - - -
    c. **User Story**: Final Project Report Documentation  
    
    **Executed by**: _Sudipto Sarkar, Arnab KarSarkar, Ujjal Saha, _
    - - - -
    c. **User Story**: Final Project Report Documentation  
    
    **Executed by**: _Ujjal Saha, Sudipto Sarkar, Arnab KarSarkar_

