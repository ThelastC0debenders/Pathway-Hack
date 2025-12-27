import pathway as pw
from pathway_engine.ingestion.loader import load_file


def watch_local_folder(folder_path: str, **kwargs):
    table = pw.io.fs.read(
        folder_path,
        format="binary",
        autocommit_duration_ms=1000,
        **kwargs,
    )

    parsed = table.select(
        content=pw.apply(load_file, table.data),
    )

    return parsed
