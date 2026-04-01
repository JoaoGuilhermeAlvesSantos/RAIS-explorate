from pathlib import Path
import csv
import re
from difflib import SequenceMatcher

DATA_DIR = Path(__file__).resolve().parent / "data"
IFDM_PATH = DATA_DIR / "ifdm_2023.csv"
MUNICIPIOS_PATH = DATA_DIR / "municipios_localidade.csv"
OUTPUT_PATH = DATA_DIR / "ifdm_2023_codigo_ibge.csv"


def normalize_text(value):
    if value is None:
        return ""
    text = str(value).strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def compare_score(a, b):
    return SequenceMatcher(None, a, b).ratio()


def load_municipios(municipios_path):
    municipalities = []
    with municipios_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["sigla_uf"] = row.get("sigla_uf", "").strip()
            row["nome_norm"] = normalize_text(row.get("nome", ""))
            municipalities.append(row)
    return municipalities


def load_ifdm(ifdm_path):
    rows = []
    with ifdm_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["UF"] = row.get("UF", "").strip()
            row["Município"] = row.get("Município", "").strip()
            rows.append(row)
    return rows, reader.fieldnames


def build_lookup(municipalities):
    lookup = {}
    for row in municipalities:
        uf = row["sigla_uf"]
        if not uf:
            continue
        lookup.setdefault(uf, {})[row["nome_norm"]] = row
    return lookup


def best_match_name(name_norm, candidates):
    best_score = 0.0
    best_row = None
    best_length_diff = None
    for candidate in candidates:
        candidate_norm = candidate["nome_norm"]
        score = compare_score(name_norm, candidate_norm)
        length_diff = abs(len(name_norm) - len(candidate_norm))
        if best_row is None:
            best_row = candidate
            best_score = score
            best_length_diff = length_diff
            continue

        if score > best_score or (score == best_score and length_diff < best_length_diff):
            best_score = score
            best_row = candidate
            best_length_diff = length_diff

    return best_score, best_row, best_length_diff


def write_output(rows, fieldnames, output_path):
    if "codigo_ibge" not in fieldnames:
        fieldnames = fieldnames + ["codigo_ibge"]
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    municipalities = load_municipios(MUNICIPIOS_PATH)
    lookup = build_lookup(municipalities)
    ifdm_rows, fieldnames = load_ifdm(IFDM_PATH)

    total = len(ifdm_rows)
    unmatched = []
    exact = 0
    fuzzy = 0
    low_confidence = 0

    for row in ifdm_rows:
        uf = row["UF"]
        name = row["Município"]
        name_norm = normalize_text(name)
        row["codigo_ibge"] = ""

        candidates_by_uf = lookup.get(uf, {})
        if not candidates_by_uf:
            unmatched.append((name, uf, "no-state"))
            continue

        direct = candidates_by_uf.get(name_norm)
        if direct is not None:
            row["codigo_ibge"] = direct.get("codigo_ibge", "")
            exact += 1
            continue

        candidates = [cand for cand in municipalities if cand["sigla_uf"] == uf]
        score, best, length_diff = best_match_name(name_norm, candidates)
        if best is None:
            unmatched.append((name, uf, "no-candidate"))
            continue

        if score < 0.80 or length_diff > 3:
            low_confidence += 1
            unmatched.append((name, uf, f"low-score={score:.3f}; len-diff={length_diff}; matched={best.get('nome')}"))
            continue

        row["codigo_ibge"] = best.get("codigo_ibge", "")
        fuzzy += 1

    write_output(ifdm_rows, fieldnames, OUTPUT_PATH)

    print(f"Total rows processed: {total}")
    print(f"Exact matches: {exact}")
    print(f"Fuzzy matches: {fuzzy}")
    print(f"Low-confidence matches: {low_confidence}")
    if unmatched:
        print("Some rows were unmatched or low confidence. See sample below:")
        for sample in unmatched[:20]:
            print(sample)
        if len(unmatched) > 20:
            print(f"... and {len(unmatched) - 20} more")
    else:
        print("All rows matched successfully.")
    print(f"Output written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
