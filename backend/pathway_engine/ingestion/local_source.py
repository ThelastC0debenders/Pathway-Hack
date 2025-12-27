import pathway as pw
from pathway_engine.ingestion.loader import load_file


def watch_local_folder(folder_path: str):
    table = pw.io.fs.read(
        folder_path,
        format="binary",
        autocommit_duration_ms=1000,

        ignore=[
            ".git/**",
            "**/.git/**",
            "__pycache__/**",
            "**/__pycache__/**",
            "*.pyc",
            "*.log",
        ],
    )

    parsed = table.select(
        content=pw.apply(load_file, table.data),
        path=table.path,        # useful for diff & attribution
        modified_at=table.time  # Pathway-provided timestamp
    )

    return parsed
