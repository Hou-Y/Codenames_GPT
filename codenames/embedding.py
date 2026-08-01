from sentence_transformers import SentenceTransformer

model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)

# debug
doc_vec = model.encode("search_document: APPLE")
query_vec = model.encode("search_query: fruit")


#debug
for name, kwargs in [
    ("nomic-ai/nomic-embed-text-v1.5", {"trust_remote_code": True}),
]:
    m = SentenceTransformer(name, **kwargs)
    v = m.encode("APPLE")
    print(name, v.shape)