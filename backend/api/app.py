from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
from huggingface_hub import hf_hub_download

from app.data_loader import load_colors
from app.color_detection import load_lexicon, detect_named_colors
from app.keyword_matcher import extract_constraints
from app.filtering import filter_candidates
from app.ranking import load_ranking_resources, rank_candidates
from app.palette_builder import build_palette

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return "hello"



df = load_colors()

lexicon, reverse_index = load_lexicon("data/lexicon.pickle")

embeddings_path = hf_hub_download(
    repo_id="aarish8115/color-palette-assets",
    filename="data/embeddings.npy"
)

model, embeddings = load_ranking_resources(
    embeddings_path,
    "BAAI/bge-small-en-v1.5"
)
valid_hue_families = {
    value.strip().lower()
    for value in df["hue_family"].dropna().astype(str)
    if value.strip()
}


class PaletteRequest(BaseModel):
    prompt: str
    palette_type: Literal["subtle","monochrome",'complementary',"analogous","triadic","vibrant"]
    num_colors: Literal[2,3,4,5,6]


@app.post("/generate-palette")
def generate_palette(request: PaletteRequest):
    prompt = request.prompt
    palette_type = request.palette_type
    num_colors = request.num_colors

    color_result = detect_named_colors(prompt, lexicon, reverse_index)
    constraints = extract_constraints(prompt, valid_hue_families)
    filtered = filter_candidates(df, constraints, color_result["matched_row_ids"])

    if filtered.empty:
        return {"palette": [], "message": "No matching colors found."}

    ranked = rank_candidates(filtered, prompt, embeddings, model)

    palette = build_palette(
        df, ranked, constraints,
        color_result["matched_words"], color_result["matched_row_ids"],
        palette_type, num_colors
    )

    return {
        "palette": [
            {
                "role": role,
                "name": row["color_name"],
                "hex": row["hex"],
                "hue": float(row["Hue"]),
                "saturation": float(row["Saturation"]),
                "lightness": float(row["Lightness"]),
            }
            for role, row in palette
        ]
    }