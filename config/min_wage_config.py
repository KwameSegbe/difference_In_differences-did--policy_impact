from dataclasses import dataclass
import diff_diff


@dataclass(frozen=True)
class MinWageConfig:
    url: str = "https://www.dol.gov/agencies/whd/state/minimum-wage/history"
    table_index: int = 0
    output_filename: str = "min_wage_raw.csv"