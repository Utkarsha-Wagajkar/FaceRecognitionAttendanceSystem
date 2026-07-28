from insightface.app import FaceAnalysis

# -----------------------------
# Load InsightFace Model
# -----------------------------
def load_face_model():

    print("Loading InsightFace Model...")

    app = FaceAnalysis()
    app.prepare(ctx_id=0)

    print("✅ InsightFace Loaded!")

    return app