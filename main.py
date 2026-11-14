import json
import os
from pathlib import Path

def main():
    in_dir = Path(os.environ.get("MAKEFUN_INPUT_DIR", "/input"))
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    for case_file in sorted(in_dir.glob("*.in")):
        case = json.loads(case_file.read_text())
        prices = case["markets"][0]["prices"]
        window = prices[-5:]
        guess = sum(window) / len(window)
        guess = min(9999999.99999, max(0.00001, guess))
        guess = round(guess, 5)
        row = {"case": case["case"], "price": guess}
        (out_dir / (case_file.stem + ".out")).write_text(
            json.dumps({"forecasts": [row]}))

main()
