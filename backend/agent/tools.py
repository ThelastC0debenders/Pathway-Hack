from pathway_engine.query.context_builder import build_context


def fetch_live_context(retriever):
    docs = retriever.get_latest_documents()
    return build_context(docs)
