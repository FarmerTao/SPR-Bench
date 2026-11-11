from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent
for name in ['build.py','validate.py','robustness.py','test_scoring.py','scoring_docs.py','rubric_docs.py','package_docs.py']:
 subprocess.run([sys.executable,str(here/name)],check=True)
