from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parent
ABATES_AVES_DIR = ROOT / "2023" / "abates-aves"
ABATES_SUINOS_DIR = ROOT / "2023" / "abates-suinos"
OUTPUT_CSV = ROOT / "data" / "vinculos_por_municipio_abates.csv"


def parse_int(value):
    if value is None:
        return 0
    try:
        return int(str(value).strip())
    except ValueError:
        try:
            return int(float(str(value).strip()))
        except ValueError:
            return 0


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def aggregate_files(file_paths):
    aggregated = {}
    for path in file_paths:
        records = load_json(path)
        for row in records:
            municipio = str(row.get("municipio", "")).strip()
            if municipio == "" or municipio.upper() == "TOTAL":
                continue
            total_vinculos = parse_int(row.get("total_vinculos", 0))
            municipio_nome = row.get("municipio_nome") or row.get("municipio_nome", "")
            key = municipio
            if key not in aggregated:
                aggregated[key] = {
                    "municipio": municipio,
                    "municipio_nome": municipio_nome or "",
                    "total_vinculos": 0,
                }
            aggregated[key]["total_vinculos"] += total_vinculos
            if not aggregated[key]["municipio_nome"] and municipio_nome:
                aggregated[key]["municipio_nome"] = municipio_nome

    return aggregated


def write_csv(aggregated, output_path):
    rows = sorted(aggregated.values(), key=lambda item: item["municipio"])
    fieldnames = ["municipio", "municipio_nome", "total_vinculos"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    abates_aves_files = sorted(ABATES_AVES_DIR.glob("*.json"))
    suinos_files = [
        ABATES_SUINOS_DIR / "matadouro-abate_suinos_sob_contrato.json",
        ABATES_SUINOS_DIR / "frigorifico-abate_suinos.json",
    ]
    file_paths = [*abates_aves_files, *suinos_files]

    aggregated = aggregate_files(file_paths)
    write_csv(aggregated, OUTPUT_CSV)
    print(f"Escrito {len(aggregated)} municípios em {OUTPUT_CSV}")
    for path in file_paths:
        print(f"  - {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
