import neuralcoref
import spacy
import uvicorn
from fastapi import FastAPI, Body
from pydantic import BaseModel

import coref_api.utils as utils

app = FastAPI(title="Coreference Resolution")


class TextIn(BaseModel):
    text: str


nlp = spacy.load("en_core_web_sm")
neuralcoref.add_to_pipe(nlp, greedyness=0.5, max_dist=50, blacklist=False)


@app.post("/coref")
def coref(text: TextIn = Body(...)):
    # text = text.text
    doc = nlp(text.text)
    clusters = doc._.coref_clusters
    resolved, questions = utils.get_resolved(doc, clusters)
    # resolved_coref = doc._.coref_resolved
    return {"resolved_text": resolved}


if __name__ == "__main__":
    uvicorn.run("coref_api.main:app")
