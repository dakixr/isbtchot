from pathlib import Path
import warnings

# Ignore specific warning categories, in this case, FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)

root_path: Path = Path(__file__).parent