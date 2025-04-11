#!/usr/bin/env python

import argparse
import sys
from pathlib import Path
import subprocess
import configparser

DEFAULT_SQLFLUFF_LARGE_FILE_SKIP_BYTE_LIMIT: int = 20000  # 20kB


def parse_arguments() -> argparse.Namespace:
    """Parse CLI arguments for SQLFluff checks."""
    parser = argparse.ArgumentParser(
        description='Check SQL files with sqlfluff for parsing and/or formatting.'
    )
    parser.add_argument(
        'files',
        metavar='FILE',
        type=str,
        nargs='+',
        help='SQL file(s) to check',
    )
    parser.add_argument(
        '--parse',
        action='store_true',
        help='Check SQL parsing using sqlfluff parse',
    )
    parser.add_argument(
        '--format',
        action='store_true',
        help='Check SQL formatting using sqlfluff format; if not formatted, the file is updated and exit code is 1',
    )
    return parser.parse_args()


def get_large_file_limit() -> int:
    """Get the large file skip byte limit from the .sqlfluff configuration file. Return 0 if there is no limit."""
    sqlfluff_path = Path('.sqlfluff')
    if not sqlfluff_path.exists():
        return DEFAULT_SQLFLUFF_LARGE_FILE_SKIP_BYTE_LIMIT

    config = configparser.ConfigParser()
    config.read(str(sqlfluff_path))

    try:
        limit = int(
            config['sqlfluff'].get(
                'large_file_skip_byte_limit',
                DEFAULT_SQLFLUFF_LARGE_FILE_SKIP_BYTE_LIMIT,
            )
        )
    except (ValueError, KeyError):
        limit = DEFAULT_SQLFLUFF_LARGE_FILE_SKIP_BYTE_LIMIT

    return limit


def check_large_files(files: list[Path], limit_bytes: int) -> int:
    """Checks all files in the list for size and returns 1 if any file is larger than the limit.
    If limit_bytes<=0 or smaller, there is no file limit.

    Args:
        files (list[Path])
        limit_bytes (int): filesize limit in kilobytes

    Returns:
        int: 0 if all files are within the limit, 1 if any file exceeds the limit.
    """
    errors: list[str] = []
    if limit_bytes <= 0:
        return 0

    for file_path in files:
        if file_path.stat().st_size > limit_bytes:
            errors.append(
                f"File too large ({file_path.stat().st_size} > {limit_bytes} bytes): {file_path}"
            )

    if errors:
        for error in errors:
            print(error)
        return 1

    return 0


def parse_sql_files(files: list[Path]) -> int:
    """Parse SQL files with sqlfluff and return appropriate exit code.

    Args:
        files (list[Path]): List of SQL files to parse.

    Returns:
        int: 0 if all files parse successfully, 1 otherwise.
    """
    errors: list[str] = []

    for file_path in files:
        if not file_path.exists():
            errors.append(f"File not found: {file_path}")
            continue

        cmd = [sys.executable, '-m', 'sqlfluff', 'parse', str(file_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            errors.append(f"Parsing failed for {file_path}:\n{result.stderr}")

    if errors:
        for error in errors:
            print(error)
        return 1

    return 0


def format_sql_files(files: list[Path]) -> int:
    """Format SQL files with sqlfluff and return appropriate exit code.

    If a file is not formatted correctly, the file is updated and an error is reported.

    Args:
        files (list[Path]): List of SQL files to format.

    Returns:
        int: 0 if all files are formatted correctly, 1 otherwise.
    """
    errors: list[str] = []

    for file_path in files:
        if not file_path.exists():
            errors.append(f"File not found: {file_path}")
            continue

        # Run the sqlfluff format command which both checks and formats the file
        cmd = [sys.executable, '-m', 'sqlfluff', 'format', str(file_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            errors.append(f"Formatting issue for {file_path}:\n{result.stderr}")

    if errors:
        for error in errors:
            print(error)
        return 1

    return 0


def main() -> None:
    """Main entry point for CLI execution."""
    sqlfluff_path = Path('.sqlfluff')
    if not sqlfluff_path.exists():
        print('A .sqlfluff configuration file is required for this script in this directory.')
        sys.exit(1)

    args = parse_arguments()
    sql_files = [Path(file) for file in args.files if file.endswith('.sql')]

    if not sql_files:
        print('No SQL files to check.')
        sys.exit(0)

    if not args.parse and not args.format:
        print('No action requested, please use --parse and/or --format.')
        sys.exit(1)

    large_file_limit_bytes = get_large_file_limit()
    large_file_exit = check_large_files(sql_files, large_file_limit_bytes)
    if large_file_exit != 0:
        sys.exit(large_file_exit)

    if args.parse:
        parse_exit = parse_sql_files(sql_files)
        if parse_exit != 0:
            sys.exit(parse_exit)

    if args.format:
        format_exit = format_sql_files(sql_files)
        if format_exit != 0:
            sys.exit(format_exit)

    sys.exit(0)


if __name__ == '__main__':
    main()
