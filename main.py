from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, requests
import openai
import random
from dotenv import load_dotenv
from movies import movie_titles 

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
omdbKey= os.getenv("ODMB_API_KEY")
app = FastAPI()



def getRandomMovie():
        random_result = random.choice(movie_titles)
        response = requests.get(f"http://www.omdbapi.com/?t={random_result}&apikey={omdbKey}").json()
        return {
            "title": response["Title"],
            "plot": response["Plot"]
        }






@app.post("/rewrite-plot/")
async def rewrite_plot():
    req =getRandomMovie()
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You're a witty and creative storyteller. "
                        "Your task is to take a movie name and its plot, and rewrite it in a fun, playful, and imaginative way. "
                        "Add humor, exaggeration, and quirky commentary where appropriate. "
                        "Make it engaging and entertaining, as if you are playing guess the movie by plot with a friend over coffee."
                        "*Do not reveal the movie name anywhere in the story*"
                    )
                },
                {
                    "role": "user",
                    "content": (
                    f"Movie Name: {req['title']}\n"
f"Original Plot: {req['plot']}\n\n"

                        "Now rewrite the plot in your fun style!"
                    )
                }
            ],
            temperature=0.9,
            max_tokens=1000
        )

        return {
            "fun_plot": response.choices[0].message.content.strip(),
            "movie": req['title']
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
