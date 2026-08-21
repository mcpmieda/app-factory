import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import http from "node:http";
import path from "node:path";

const root = path.resolve("dist");
http
  .createServer(async (request, response) => {
    try {
      const requested = new URL(request.url ?? "/", "http://127.0.0.1")
        .pathname;
      let file = path.join(root, requested);
      if ((await stat(file)).isDirectory())
        file = path.join(file, "index.html");
      const type = file.endsWith(".css")
        ? "text/css"
        : "text/html; charset=utf-8";
      response.writeHead(200, { "content-type": type });
      createReadStream(file).pipe(response);
    } catch {
      response.writeHead(404).end("Not found");
    }
  })
  .listen(4321, "127.0.0.1", () => console.log("static site ready"));
