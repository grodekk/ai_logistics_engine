import argparse
import json
import subprocess
from pathlib import Path


ENDPOINTS = [
    "/health",
    "/routes/available",
    "/analytics/monthly-expenses",
    "/analytics/top-late-clients",
    "/analytics/pareto-route-costs",
    "/clients/scores",
]

CONCURRENCIES = [1, 5, 10, 20]


def run_oha(url, requests, concurrency):
    command = [
        "oha",
        "-n", str(requests),
        "-c", str(concurrency),
        "--no-tui",
        "--output-format", "json",
        url,
    ]

    process = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )

    return json.loads(process.stdout)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--label",
        required=True,
        choices=["sync", "async"],
    )

    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
    )

    parser.add_argument(
        "--requests",
        type=int,
        default=5000,
    )

    parser.add_argument(
        "--rounds",
        type=int,
        default=3,
    )

    parser.add_argument(
        "--output",
        required=True,
    )

    args = parser.parse_args()

    results = []

    for endpoint in ENDPOINTS:
        url = args.base_url.rstrip("/") + endpoint

        for concurrency in CONCURRENCIES:
            for round_number in range(1, args.rounds + 1):

                print(
                    f"{args.label} "
                    f"{endpoint} "
                    f"c={concurrency} "
                    f"round={round_number}"
                )

                oha_result = run_oha(
                    url=url,
                    requests=args.requests,
                    concurrency=concurrency,
                )

                result = {
                    "label": args.label,
                    "endpoint": endpoint,
                    "concurrency": concurrency,
                    "round": round_number,
                    "requests": args.requests,
                    "oha": oha_result,
                }

                results.append(result)

                summary = oha_result["summary"]

                print(
                    f"RPS={summary['requestsPerSec']:.2f} "
                    f"avg={summary['average'] * 1000:.2f} ms"
                )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)


if __name__ == "__main__":
    main()