# btc-cent-forecast-01: forecast BTC 240 minutes ahead of each checkpoint.
# The scorer pays absolute error in cents, so the best guess is our honest middle
# estimate of the future close: the recorder's closes carry small sampling noise around
# the true mid-price, so we smooth the last five closes (a light average, not a trend
# model), then clamp and round on the price grid exactly like the house baseline.
import json
import os
from pathlib import Path

def main():
    in_dir = Path(os.environ.get("MAKEFUN_INPUT_DIR", "/input"))
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    for case_file in sorted(in_dir.glob("*.in")):  # one case per graded run
        case = json.loads(case_file.read_text())
        prices = case["markets"][0]["prices"]
        window = prices[-5:]
        guess = sum(window) / len(window)
        guess = min(9999999.99999, max(0.00001, guess))
        guess = round(guess, 5)
        row = {"case": case["case"], "price": guess}
        (out_dir / (case_file.stem + ".out")).write_text(  # one forecast row per case
            json.dumps({"forecasts": [row]}))

main()
