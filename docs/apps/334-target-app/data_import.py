from pathlib import Path
import pandas as pd

app_dir = Path(__file__).parent
scores = pd.read_csv(app_dir / "scores.csv")