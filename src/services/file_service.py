import pandas as pd
from src.utils.mongo_utils import enrich_data

def sanitize_data(data):
    return data.applymap(lambda x: x.strip().replace("\s+", " ") if isinstance(x, str) else x)

def process_csv(file_path):
    df = pd.read_csv(file_path)
    df_cleaned = sanitize_data(df)
    df_enriched = pd.DataFrame(enrich_data(df_cleaned.to_dict(orient="records")))

    processed_file = file_path.replace(".csv", "_processed.xlsx")
    df_enriched.to_excel(processed_file, index=False)

    return processed_file
