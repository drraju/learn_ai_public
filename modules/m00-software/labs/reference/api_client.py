"""Read the local teaching API and validate basic response structure."""
import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


def fetch_documents(port: int, extension: str | None = None) -> dict:
    query = urlencode({"extension": extension}) if extension is not None else ""
    url = f"http://127.0.0.1:{port}/documents"
    if query:
        url += "?" + query
    with urlopen(url, timeout=5) as response:
        payload = json.load(response)
    if not isinstance(payload, dict):
        raise ValueError("expected a JSON object")
    rows = payload.get("documents")
    if not isinstance(rows, list):
        raise ValueError("expected a documents array")
    if type(payload.get("count")) is not int or payload["count"] != len(rows):
        raise ValueError("count does not match documents")
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("expected document objects")
        for key in ("path", "name", "extension", "modified_utc"):
            if not isinstance(row.get(key), str):
                raise ValueError(f"invalid text field: {key}")
        if type(row.get("size_bytes")) is not int or row["size_bytes"] < 0:
            raise ValueError("invalid size_bytes")
    if not isinstance(payload.get("warnings"), list):
        raise ValueError("expected a warnings array")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--extension")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    try:
        print(json.dumps(fetch_documents(args.port, args.extension), indent=2))
        return 0
    except HTTPError as error:
        print(f"HTTP failure: {error.code}", file=sys.stderr)
    except (URLError, TimeoutError, OSError) as error:
        print(f"Connection failure: {error}", file=sys.stderr)
    except (ValueError, UnicodeError) as error:
        print(f"Invalid response: {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
