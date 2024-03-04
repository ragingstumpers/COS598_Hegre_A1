import argparse
from collections import defaultdict
import csv


def _read_results_csv(filepath: str, years: set[int]) -> dict[str, dict[int, dict[str, float]]]:
    # ["COUNTRY", "YEAR", "NONE", "MINOR", "MAJOR", "EITHER"
    with open(filepath, mode="r", newline='') as csv_file:
        # first row is interpreted as keys
        reader = csv.DictReader(csv_file)
        # {country: {Year: {conflict: percentage}}}
        country_to_year_to_conflict_percentages = defaultdict(lambda: defaultdict(lambda: {}))
        for row in reader:
            year = int(row["YEAR"])
            if year not in years:
                continue
            country = row['COUNTRY']
            for lvl in ("MINOR", "MAJOR", "EITHER"):
                country_to_year_to_conflict_percentages[country][year][lvl] = float(row[lvl])
        return country_to_year_to_conflict_percentages
    
def _write_results_csv(
        filepath: str,
        years: set[int],
        num_countries: int,
        country_to_year_to_conflict_percentages: dict[str, dict[int, dict[str, float]]]
    ) -> None:
    sort_by_year = min(years)
    sorted_countries = sorted(
        [
            (country, year_to_conflict_percentages)
            for country, year_to_conflict_percentages in country_to_year_to_conflict_percentages.items()
        ],
        key=lambda a: -1*a[1][sort_by_year]["EITHER"]
    )[:num_countries]
    with open(filepath, "w+") as csv_file:
        writer = csv.writer(csv_file)
        cols = ["COUNTRY"]
        for year in sorted(years):
            for col in ("MINOR", "MAJOR", "EITHER"):
                total_col = f"{col}_{year}"
                cols.append(total_col)
    
        writer.writerow(cols)
        for country, year_to_conflict_percentages in sorted_countries:
            row = [country]
            for year in sorted(years):
                for col in ("MINOR", "MAJOR", "EITHER"):
                    row.append(year_to_conflict_percentages[year][col])
            writer.writerow(row)


def _main():
    sim_cli = argparse.ArgumentParser(description="A program to print the top N countries probability of conflict.")
    sim_cli.add_argument(
        "-est", "--estimated_conflicts",
        type=str, help="filepath to a CSV file outputted by run_simulation.py", required=True,
    )
    sim_cli.add_argument(
        "-n", "--num_countries",
        type=int, help="the number of countries to return in the results", required=True,
    )
    sim_cli.add_argument(
        "-years", "--years_list",
        nargs='*', type=int, help="the three years to output for, order will be sorted by value for first year", required=True,
    )
    sim_cli.add_argument(
        "-out", "--output_destination",
        type=str, help="filepath to write the results to in CSV format", required=True,
    )

    args = sim_cli.parse_args()
    years_set = set(args.years_list)
    country_to_year_to_conflict_percentages = _read_results_csv(
        args.estimated_conflicts,
        years_set
    )
    return _write_results_csv(
        args.output_destination, years_set, args.num_countries, country_to_year_to_conflict_percentages
    )


if __name__ == '__main__':
   _main()

# python get_top.py -est ~/Desktop/original_models/results.csv -n 30 -years 2017 2030 2050 -out ~/Desktop/original_models/top_30.csv
