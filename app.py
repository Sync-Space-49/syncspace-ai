import json
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from flask import Flask, jsonify, request

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

client = OpenAI()
app = Flask(__name__)

@app.get("/")
def hello_world():
  return {"hello": "world"}

@app.post("/api/generate/board")
def generate_board():
  title=request.form.get('title')
  description=request.form.get('description')
  detail_level=request.form.get('detail_level') or 'detailed'
  story_point_type=request.form.get('story_point_type') or 'Fibonacci Sequence'
  story_points=request.form.get('story_points') or '0, 1, 2, 3, 5'

  query = f'''
    I'm making a project titled "{title}" with the description "{description}". Create me a {detail_level} storyboard with cards describing what needs to be done to complete the entire project from beggining to end in the following JSON format: 
  {{
  "Sprint title with high-level overview": [ 
  {{
  "title": "briefly describes the story item", 
  "description": "gives more detail if more context is needed", 
  "story_points" "points based on complexity which are in the {story_point_type} format ({story_points})", 
  "assigned": ["leave this empty"] 
  }},
  ]
  }}, 
  '''

  response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {
            "role": "user",
            "content": query,
        },
    ],
    response_format={ "type": "json_object" }
  )

  if response.choices[0].finish_reason == "stop":
    results = response.choices[0].message.content
    parsed_result = json.loads(results)
    return jsonify(parsed_result)
  else:
    result = response.choices[0].finish_reason
    return jsonify({"message": result})

# @app.post("/api/generate/stack")
# def generate_stack():
#   return jsonify({"hello": "world"})

# @app.post("/api/generate/card")
# def generate_card():
#   return jsonify({"hello": "world"})
