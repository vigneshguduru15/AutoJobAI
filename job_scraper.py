import os, requests, random, logging
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.INFO)

try:
    from streamlit import secrets
    API_KEY = secrets["rapidapi"]["api_key"]
except:
    API_KEY = os.getenv("RAPIDAPI_KEY")

HOST = "jsearch.p.rapidapi.com"
COUNTRIES = {"India":"in","United States":"us","United Kingdom":"gb","Canada":"ca","Remote":"us"}

def get_jobs(query="Software Engineer", location="India"):
    if not API_KEY:
        logging.error("Missing RapidAPI key.")
        return []
    url = f"https://{HOST}/search"
    params = {"query":f"{query} in {location}","page":random.randint(1,3),"num_pages":1,"country":COUNTRIES.get(location,"us")}
    headers = {"X-RapidAPI-Key":API_KEY,"X-RapidAPI-Host":HOST}
    try:
        r = requests.get(url, params=params, headers=headers)
        if r.status_code != 200: return []
        data = r.json().get("data",[])
        for j in data:
            j["title"] = j.get("job_title","No Title")
            j["company_name"] = j.get("employer_name","Unknown")
            j["description"] = j.get("job_description","")
            j["apply_link"] = j.get("job_apply_link") or j.get("job_posting_url") or "#"
        return data
    except Exception as e:
        logging.error(e)
        return []
