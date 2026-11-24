"""Local teaching API. Do not expose this server to a public network."""
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from catalogue import normalise_extension, scan_directory


def make_handler(root: Path):
    class Handler(BaseHTTPRequestHandler):
        def respond(self, status, payload):
            encoded = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def do_GET(self):
            parts = urlsplit(self.path)
            if parts.path == "/health":
                self.respond(200, {"status": "ok"})
                return
            if parts.path != "/documents":
                self.respond(404, {"error": "unknown route"})
                return
            params = parse_qs(parts.query, keep_blank_values=True)
            if set(params) - {"extension"}:
                self.respond(400, {"error": "unknown query parameter"})
                return
            try:
                values = params.get("extension")
                if values is not None and len(values) != 1:
                    raise ValueError("supply extension only once")
                extension = normalise_extension(values[0]) if values else None
            except ValueError as error:
                self.respond(400, {"error": str(error)})
                return
            try:
                records, warnings = scan_directory(root)
                if extension is not None:
                    records = [row for row in records
                               if row["extension"] == extension]
                self.respond(200, {"count": len(records), "documents": records,
                                   "warnings": warnings})
            except (OSError, ValueError):
                logging.exception("Local sample scan failed")
                self.respond(500, {"error": "sample directory unavailable"})

        def log_message(self, fmt, *args):
            # This teaching service has no secrets in its sample query strings.
            logging.info(fmt, *args)

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("sample_docs"))
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    if not args.root.is_dir():
        parser.error("root must be an existing sample directory")
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    with HTTPServer(("127.0.0.1", args.port), make_handler(args.root.resolve())) as server:
        logging.info("Teaching API on http://127.0.0.1:%d", args.port)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            logging.info("Stopped")


if __name__ == "__main__":
    main()
