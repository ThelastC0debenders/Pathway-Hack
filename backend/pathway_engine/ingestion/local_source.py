import pathway as pw
from pathway_engine.ingestion.loader import load_file


def watch_local_folder(folder_path: str):
    """
    Streams file updates from a local folder.
    """

    table = pw.io.fs.read(
        folder_path,
        format="binary",
        autocommit_duration_ms=1000,
    )

    parsed = table.select(
        content=pw.apply(load_file, table.data),
    )

    return parsed
