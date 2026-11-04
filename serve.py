#!/usr/bin/env python3
"""
Mahler Symphony No. 2 ("Resurrection") — Symphony Atlas Local Streaming Server
Supports HTTP 206 Partial Content byte-range requests for accurate audio scrubbing.
Usage: python3 serve.py [port]
"""

import os
import re
import sys
import mimetypes
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class RangeRequestHandler(SimpleHTTPRequestHandler):
    """HTTP request handler with RFC 7233 Byte-Range (HTTP 206) support."""

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()

        ctype = self.guess_type(path)
        try:
            f = open(path, "rb")
        except OSError:
            self.send_error(404, "File not found")
            return None

        fs = os.fstat(f.fileno())
        file_len = fs.st_size
        range_header = self.headers.get("Range")

        if range_header:
            match = re.match(r"bytes=(\d+)-(\d*)", range_header)
            if match:
                start = int(match.group(1))
                end = int(match.group(2)) if match.group(2) else file_len - 1
                end = min(end, file_len - 1)
                if start >= file_len or start > end:
                    self.send_response(416, "Requested Range Not Satisfiable")
                    self.send_header("Content-Range", f"bytes */{file_len}")
                    self.end_headers()
                    f.close()
                    return None

                length = end - start + 1
                self.send_response(206, "Partial Content")
                self.send_header("Content-type", ctype)
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Range", f"bytes {start}-{end}/{file_len}")
                self.send_header("Content-Length", str(length))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                f.seek(start)
                self._range_bytes_remaining = length
                return f

        self.send_response(200)
        self.send_header("Content-type", ctype)
        self.send_header("Content-Length", str(file_len))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self._range_bytes_remaining = None
        return f

    def copyfile(self, source, outputfile):
        remaining = getattr(self, "_range_bytes_remaining", None)
        if remaining is None:
            return super().copyfile(source, outputfile)
        bufsize = 64 * 1024
        while remaining > 0:
            chunk = source.read(min(bufsize, remaining))
            if not chunk:
                break
            outputfile.write(chunk)
            remaining -= len(chunk)


def run(port: int = 8080):
    mimetypes.add_type("audio/midi", ".mid")
    mimetypes.add_type("application/javascript", ".js")
    mimetypes.add_type("application/json", ".json")
    server = ThreadingHTTPServer(("0.0.0.0", port), RangeRequestHandler)
    print(f"Mahler 2 Symphony Atlas streaming server listening at http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.server_close()


if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run(port_arg)
