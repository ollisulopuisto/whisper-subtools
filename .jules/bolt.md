## 2026-11-17 - Rejected: batching per-segment writes in json-to-text.py

**Learning:** Replacing one `outfile.write()` call per transcript segment with a single joined write is not a win. At 20k segments the median was 47.03 ms (original) vs 48.88 ms (batched) — inside run-to-run noise. At 200k segments: 249.75 ms vs 250.86 ms median, tight stdev (~4 ms) and fully overlapping distributions. `json.load` parsing and per-segment string formatting dominate runtime; I/O syscall count is not the bottleneck here.

**Action:** Do not retry write-batching on this script. A future optimization pass should target `json.load`/segment formatting, or accept the CLI is already fast enough. Always baseline with multiple repetitions plus a cold-run outlier check before concluding.
