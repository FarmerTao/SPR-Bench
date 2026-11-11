# Contributing

Use English for code, task prompts and benchmark documentation. Use Python 3.12
and install requirements-dev.txt. Edit canonical files in tools/, then rebuild
with tools/ingest.py, tools/build.py and tools/docs.py. Generated copies must match.
Run tools/check_repository.py and tools/validate.py before submitting.
Local validation executes trusted code only; never run an unknown submission on
your host. Use isolated disposable containers for untrusted agents.

Every new dataset needs an experimentally verified origin, clear redistribution
rights, source/derived hashes, exact extraction coordinates and documented assay
scope. Simulated curves, fitted predictions, image reconstructions and fabricated
negative labels are not eligible for this experimental task set. Any separate
simulation track must be explicitly named and excluded from real-data scores.

Scoring changes need documented behavior, regression checks, version changes and
honest scientific limitations. Never hand-edit expected results to make a solver
pass. Add independent expert review before claiming biological decision validity.
Preserve original source licenses and attribution. Code contributions are MIT
licensed; third-party data retain their own licenses.

Pull requests should explain the problem, resulting behavior and validation.
Do not commit credentials, private evaluation data or unrelated run logs.
