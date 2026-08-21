# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import Optional

# from data_loader import load_colors
# from color_detection import load_lexicon, detect_named_colors
# from keyword_matcher import extract_constraints
# from filtering import filter_candidates
# from ranking import load_ranking_resources, rank_candidates
# from palette_builder import build_palette

# app = FastAPI()

# # --- Load everything once, at startup ---
# df = load_colors()
# lexicon, reverse_index = load_lexicon("data/lexicon.pickle")
# model, embeddings = load_ranking_resources(
#     "data/embeddings.npy",
#     r"D:\Projects\Moodboard Generator\Color\backend\models\embedding"
# )


# class PaletteRequest(BaseModel):
#     prompt: str
#     palette_type: str
#     num_colors: int


# @app.post("/generate-palette")
# def generate_palette(request: PaletteRequest):
#     prompt = request.prompt
#     palette_type = request.palette_type
#     num_colors = request.num_colors

#     color_result = detect_named_colors(prompt, lexicon, reverse_index)
#     constraints = extract_constraints(prompt)
#     filtered = filter_candidates(df, constraints, color_result["matched_row_ids"])

#     if filtered.empty:
#         return {"palette": [], "message": "No matching colors found."}

#     ranked = rank_candidates(filtered, prompt, embeddings, model)

#     palette = build_palette(
#         df, ranked, constraints,
#         color_result["matched_words"], color_result["matched_row_ids"],
#         palette_type, num_colors
#     )

#     return {
#         "palette": [
#             {
#                 "role": role,
#                 "name": row["color_name"],
#                 "hex": row["hex"],
#                 "hue": float(row["Hue"]),
#                 "saturation": float(row["Saturation"]),
#                 "lightness": float(row["Lightness"]),
#             }
#             for role, row in palette
#         ]
#     }