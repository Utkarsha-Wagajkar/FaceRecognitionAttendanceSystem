from insightface.app import FaceAnalysis

print("Loading InsightFace model...")

app = FaceAnalysis()

app.prepare(ctx_id=0)

print("✅ InsightFace loaded successfully!")