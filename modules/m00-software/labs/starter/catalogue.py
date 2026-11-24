"""Your scaffold. Implement one function at a time; see the handbook."""
from pathlib import Path


def scan_directory(root: Path) -> tuple[list[dict], list[str]]:
    """Return metadata records and warnings. Reject a bad input root.

    Fields: path, name, extension, size_bytes, modified_utc.
    Direct regular files only; skip subdirectories and symlinks.
    """
    raise NotImplementedError("Start with Exercise 10")


def write_csv(records: list[dict], output: Path) -> None:
    """Write fixed columns using csv.DictWriter and UTF-8."""
    raise NotImplementedError("Then complete Exercise 11")


def main():
    records, warnings = scan_directory(Path("sample_docs"))
    print(f"Found {len(records)} documents")
    print(warnings)


if __name__ == "__main__":
    main()
