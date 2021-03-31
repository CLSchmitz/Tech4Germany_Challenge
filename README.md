# Tech4Germany_Challenge

This is my submission for the 2021 Tech4Germany coding challenge. It pulls data from the German [GovData portal](https://www.govdata.de/)'s [CKAN API](https://docs.ckan.org/en/2.8/contents.html), formats it for visualization, creates a plot and wraps it in a simple dashboard that is locally hosted.

## Get Started

To run this locally, you will need a working installation of python.

1. (Optionally) in your command prompt, create a new environment with

`python venv C:/path/to/my_env_name` and activate it with `.\my_env_name\Scripts\activate`

or, if you have a conda installation, with

`conda create -n my_env_name` and activate it with `conda activate my_env_name`. You may also need to `conda install pip` in this case.

2. Clone the git repo or download the files to a local location.
3. Navigate to the project folder and install the required packages with `pip install -r requirements.txt`
4. Run the app: `python dashboard.py`

After a few seconds, Dash outputs a message which includes the address at which the dashboard can be accessed:

```
Dash is running on http://127.0.0.1:8050/

 Warning: This is a development server. Do not use app.run_server
 in production, use a production WSGI server like gunicorn instead.

 * Serving Flask app "dashboard" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 ```

**Should this not work** because of local issues, a static version of the plot is included as a .html. This does not grab data from the API and is not used in the .py at all. 

## Structure/Tech Stack

All of the app's logic happens in app.py. There was no palpable benefit to segmenting the sections of the code into functions or different .py files, as no code is reused or duplicated. If the dashboard were to grow in size, it might make sense to split the sections modularly for readability - eg. data processing in one file and the frontend in another.

Tech Stack: 
- Python 3.9.2
- Pandas for Data Processing
- [Plotly](https://plotly.com/) for the Graphs
- [Dash](https://dash.plotly.com/) for the Dashboard.

Dash is provided by Plotly's developers and integrates tightly with it, making the stack a natural choice for a time-limited challenge like this.
