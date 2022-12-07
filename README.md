# InvestBuddy CourseProject

This is the README for InvestBuddy, a CS 410 project for UIUC. The goal of the project is to create a chatbot that can accurately answer user questions and link them to relevant financial articles.

Use the following link to view our tutorial video:
```
https://drive.google.com/drive/folders/1W3RUf-lxvOG8pIk-sg1yghiO2HrMpj0o
```

To run our website, there are several steps:
1. set up the environment
use the following link
```
https://nodejs.org/download/release/v16.18.1/
```
and download "node-v16.18.1-x64.msi" (this file can help you set up everything)

2. clone the file to local
run the following command
```
git clone https://github.com/ajhuerta/CourseProject
```

3. run the program
enter the directory __client__ and run the following command line argument.
```
npm install
npm start
```
if there occurs an error, open src/App.js, and add the following code at top:
```
import React from 'react'
import ReactDOM from 'react-dom'
```
Then, run the command line again.
```
npm start
```
