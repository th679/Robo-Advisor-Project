# Robo-Advisor-Project

Original project description: https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/projects/robo-advisor.md 

##Prerequisites

Anaconda 3.7
Python 3.7
Pip

## Installation

Use Anaconda to create and activate a new virtual environment.
Install package dependencies:

```py
pip install requests 
pip install python-dotenv 
pip install matplotlib
```

## Setup
Obtain an AlphaVantage API Key: https://www.alphavantage.co/support/#api-key

Then, create a new file in the repository called ".env" and specify your API Key in the ".env" file:

```py
API_Key = "123456"
```

## Usage

Run the recommendation script:

```py
python app/robo_advisor.py
```