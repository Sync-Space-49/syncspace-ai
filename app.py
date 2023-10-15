from dotenv import load_dotenv, find_dotenv
from flask import Flask, jsonify, request
from authlib.integrations.flask_oauth2 import ResourceProtector
import guidance
import os


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

guidance.llm = guidance.llms.OpenAI("text-davinci-003", api_key=os.environ.get('OPENAI_API_KEY'), caching=False)

app = Flask(__name__)

@app.get("/")
def hello_world():
  return {"hello": "world"}

@app.post("/api/guidance/generate/board")
def generate_board():
  title = request.form.get('title')
  description = request.form.get('description')
  detail_level = request.form.get('detail_level')
  point_system = request.form.get('point_system') or 'Fibonacci Sequence (0, 1, 2, 3, 5)'

  test = [1, 2, 3, 4, 5]
  sprint_name_query = guidance('''
    I'm making a project titled "{{title}}" with the description "{{description}}". How many sprints should I have to get started?
    {{#select "sprint_num" logprobs='logprobs'}}3{{or}}4{{or}}5{{/select}}

    Give me names for each sprint (make a maximum of {{sprint_num}} sprints):
    {{#geneach 'sprint_titles' }}
    Sprint {{@index}}: {{gen "this" max_tokens=5}}
    {{/geneach}}
  ''')

  results = sprint_name_query(title=title, description=description)
  sprint_titles = results['sprint_titles']
  sprint_titles = [title.split('\n')[0].strip() for title in sprint_titles]

  card_query = guidance('''
    I'm making a project titled "{{title}}" with the description "{{description}}". Create me a {{detail_level}} storyboard with cards describing what needs to be done to complete the project.
    Use {{point_system}} for story points:
    ```json
    "board": [
      {{#each sprint_titles}}
      {
        "{{this}}": [
          {{geneach "cards"}}
          {
            "title": "{{gen "this.title" max_tokens=7}}", 
            "description": "{{gen "this.description"}}", 
            "story_points" "{{gen "this.story_points" max_tokens=1}}", 
            "assigned": [] 
          }
          {{/geneach}}
        ]
      }
      {{/each}}
    ]
    ```
  ''')
  results = sprint_name_query(title=title, description=description, detail_level=detail_level)

  return jsonify(
    {
      "sprint_num": results["sprint_num"], 
      "sprint_titles": sprint_titles
    })

# @app.post("/api/guidance/generate/sprint")
# def generate_sprint():
#   return {"hello": "world"}

# @app.post("/api/guidance/generate/card")
# def generate_card():
#   return {"hello": "world"}
