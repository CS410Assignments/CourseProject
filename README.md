# CS410 CourseProject (Team CAHJ) - Coursera Search with ChatGPT Extension

## Project Overview



## Requirements
This project is fairly straightforward with regards to requirements on the user's machine, but there are a few baselines that are required to be hit:
- The project requires Google Chrome to work.
- The project requires ChromeDriver, maintained by Chronium, to be installed in the root directory of the project in order to enable scraping (see Step 2 under Installation Instructions, below).
- The project requires a working installation of Python to scrape new course content. The file `requirements.txt` includes the packages necessary for the script to run. If you plan to scrape new course content into the project ElasticSearch index, please ensure your Python environment satisfies these requirements. <span style="color:red">(TODO - Create requirements.txt file for Python packages)</span>
- As the extension is not deployed to the Google Chrome Web Store, it requires a local copy of the codebase on the user's computer (see Step 1 under Installation Instructions, below).


## Installation Instructions
Installing the extension is quite simple; all you need to do is download the code from GitHub and then activate the extension in Chrome.
A step-by-step guide for the above is below.:

1. Pull the code from GitHub to `desiredDirectory` using your shell:
 ```
 cd desiredDirectory
 git clone https://github.com/christianopperman/CS410_Fall2023_CourseProject_TeamCAHJ.git
 ```

2. Install the appropriate ChromeDriver for your computer's enviornment from [this linke](https://googlechromelabs.github.io/chrome-for-testing/#stable), unzip it, and move the `Google Chrome for Testing` application to the `CS410__Fall2023_CourseProject_TeamCAHJ` directory created in Step 1, above.
3. Open Google Chrome.
4. Go to the Extensions page on Google Chrome by following [this link](chrome://extensions).
5. Activate Developer Mode by toggling the switch in the upper right corner labeled `Developer mode`. <br>
![Screenshot of Devloper Mode toggle](/project/CS410_Fall2023_CourseProject_TeamCAHJ/Documentation/README_images/Chrome%20Developer%20Mode.png)
6. Load the extension from the codebase pulled to your computer in Step 1 by clicking the `Load unpacked` button in the top left corner: <br>
![Screenshot of load unpacked button](/project/CS410_Fall2023_CourseProject_TeamCAHJ/Documentation/README_images/Chrome%20Load%20Unpacked.png)
7. Select the `desiredDirectory/CS410_Fall2023_CourseProject_TeamCAHJ/ChromeExtension` directory in the popup and click `Select` <br>
![Screenshot of load unpacked button](/project/CS410_Fall2023_CourseProject_TeamCAHJ/Documentation/README_images/Chrome%20Extension%20Directory.png)
8. The extension should now be available to you in your Google Chrome Extensions list.

## Usage Instructions