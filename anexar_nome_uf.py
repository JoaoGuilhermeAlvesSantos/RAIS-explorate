from pathlib import Path
import csv
import json

DATA_DIR = Path(__file__).resolve().parent / "data"
UF_CODES_PATH = DATA_DIR / "UF_codigos.csv"
MUNICIPIOS_JSON_PATH = DATA_DIR / "municipios_localidade.json"
OUTPUT_CSV_PATH = DATA_DIR / "municipios_localidade.csv"


def load_uf_siglas(uf_codes_path):
    with uf_codes_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return {int(row["id"]): row["UF"] for row in reader}


def load_municipios(municipios_json_path):
    with municipios_json_path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def write_municipios_csv(rows, output_path):
    if not rows:
        raise ValueError("Nenhum município encontrado para salvar.")

    fieldnames = list(rows[0].keys())
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    uf_map = load_uf_siglas(UF_CODES_PATH)
    municipios = load_municipios(MUNICIPIOS_JSON_PATH)

    enriched = []
    for item in municipios:
        codigo_uf = item.get("codigo_uf")
        sigla_uf = uf_map.get(int(codigo_uf)) if codigo_uf is not None else ""
        enriched_item = dict(item)
        enriched_item["sigla_uf"] = sigla_uf or ""
        enriched.append(enriched_item)

    write_municipios_csv(enriched, OUTPUT_CSV_PATH)
    print(f"Salvo {len(enriched)} municípios em: {OUTPUT_CSV_PATH}")


if __name__ == "__main__":
    main()
