import fs from "node:fs";
import path from "node:path";
import { ZipArchive } from "archiver";
const outputDir = path.resolve("artifacts");
fs.mkdirSync(outputDir, { recursive: true });
const zipPath = path.join(outputDir, "focus-lens-v0.1.0.zip");
const output = fs.createWriteStream(zipPath);
const archive = new ZipArchive({ zlib: { level: 9 } });
archive.on("warning", (error) => {
  if (error.code !== "ENOENT") throw error;
});
archive.on("error", (error) => {
  throw error;
});
archive.pipe(output);
archive.directory(path.resolve("dist"), false);
await archive.finalize();
await new Promise((resolve, reject) => {
  output.on("close", resolve);
  output.on("error", reject);
});
console.log(`Packaged ${archive.pointer()} bytes at ${zipPath}`);
