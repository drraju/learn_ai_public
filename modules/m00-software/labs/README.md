# Software foundations lab pack

Python 3.11+; standard library only. The 14 reference tests passed on macOS Python 3.11.17 and 3.13.14 on 25 November 2026; Windows and Linux remain to be checked. All sample text is invented. No API keys, paid services, or package installation are required. Git is needed only for the Git exercises.

## Start

Open a terminal in this `labs` directory. Keep outputs outside `sample_docs`. On macOS/Linux, replace `python` with `python3` if needed; on Windows use `py -3` if `python` is unavailable.

```bash
python --version
python -c "from pathlib import Path; Path('generated').mkdir(exist_ok=True)"
python reference/catalogue.py scan sample_docs --csv generated/catalogue.csv --db generated/catalogue.db
python reference/catalogue.py search generated/catalogue.db --extension .txt
python -m unittest discover -s reference -p "test_*.py" -v
```

Expected: 3 sample records; 2 `.txt` records; 14 passing test cases. `empty.txt` has zero bytes. Timestamps depend on extraction time. Warnings indicate an incomplete scan and must be investigated.

## Learn before reading the answer

1. Read the [M00 lesson](../README.md).
2. Copy `starter/` into a new practice directory and implement its functions.
3. Compare your behaviour with `reference/` after attempting it yourself.
4. Run the local HTTP and SQLite exercises below.

From `labs`, `python starter/catalogue.py` deliberately raises `NotImplementedError` until implemented. The tests target the complete reference; adapt imports or copy tests thoughtfully when testing your own version.

## Local API

Terminal A, from labs:

```bash
python reference/api_server.py --root sample_docs --port 8765
```

Terminal B, from labs:

```bash
python reference/api_client.py --port 8765 --extension .txt
```

Stop with Control-C in terminal A. Change the port in both commands if occupied. The server binds to loopback only and is not production software. It has no authentication or TLS. Do not point it at private data or expose it publicly.

## Behaviour and limits

- Scanner reads metadata only; does not alter source documents.
- Direct children only; skips directories and symlinks.
- Per-file inspection errors produce warnings; a bad input root fails.
- CSV is overwritten at the specified output path. Use generated lab paths.
- SQLite refresh replaces only the selected root's records in a transaction.
- Repeated scans do not duplicate paths; a failing refresh rolls back.
- CSV and DB writes are not one atomic operation.
- Partial scans can replace a previous snapshot with incomplete data; heed warnings.
- Search values are bound parameters; no arbitrary SQL is accepted.
- Sample paths and modification times are machine-dependent.

## Troubleshooting

- Can't open file: check `pwd`, `ls`, and path quoting.
- No such table: scan with `--db` before searching.
- Output rejected: put CSV and database in `generated/`, outside sample input.
- Connection refused: start server first and match the port.
- Tests cannot bind a port: allow local loopback networking in your environment.

Use the [project assessment rubric](../../../assessments/rubrics/project_rubric.md) for review criteria.
