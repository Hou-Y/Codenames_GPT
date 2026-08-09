from sentence_transformers import SentenceTransformer

nomic_model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)

# debug
doc_vec = nomic_model.encode("search_document: APPLE")
query_vec = nomic_model.encode("search_query: fruit")


#debug
for name, kwargs in [
    ("nomic-ai/nomic-embed-text-v1.5", {"trust_remote_code": True}),
]:
    m = SentenceTransformer(name, **kwargs)
    v = m.encode("APPLE")
    print(name, v.shape)