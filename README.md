# JobRecommendationSystem

The topic of our project is ‘Job Recommendation System’. Being students ourselves, it’s very difficult to find the right jobs based on our resumes. Currently, we end up going through most of the job descriptions and start manually checking if the job description has the skills mentioned that match with the skills that we have. Therefore, we are trying to solve this problem by providing job recommendations based on the resume that is uploaded by the user. This way, the manual process for keyword matching based on skills is not needed anymore. 

Demo Presentation and Video: https://drive.google.com/file/d/1jN_jI4-0qTC7cz_S_diDNiNH6HTBZ1zq/view?usp=share_link


# Environment Setup:

	Go to https://nodejs.org/en/ and download version 18.12.1 LTS
	python (3.0 +)
	Install virtualenv (optional)

# Procedure to Run Frontend

Frontend (In a dedicated Terminal)
	
	cd client
	npm install
	npm start
        Open in browser http://localhost:3001/


# Procedure to Run Backend

Backend (In a separate dedicated terminal)

	cd backend
	pip install -r requirements.txt
        Install these packages separately to avoid issues while running the project if needed:  
        pip install nltk 
        pip install pyPDF2
	python server.py



