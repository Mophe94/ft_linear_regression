import csv

class CsvLoadError(Exception):
    """Raised when a CSV file cannot be loaded or is malformed."""


def load_csv(path: str) -> tuple[list[str], list[list[str]]]:
    """Load a CSV file and return its header and rows as raw strings.

    The first line of the file is the header. It defines the number of
    columns: every data row must contain exactly that many fields. Values
    are returned as strings, without any type conversion. Blank lines are skipped, 
    as pandas does by default.

    Args:
        path: Path to the CSV file to read.

    Returns:
        A tuple (header, rows) where:
            - header is the list of column names, in file order.
            - rows is a list of rows, each row being a list of strings
              with the same length as header, in file order.
        A file containing only a header returns (header, []).

    Raises:
        CsvLoadError: If the file cannot be opened or read (missing file,
            permission denied, path is a directory, invalid encoding),
            if the file is empty, if the header line is empty, or if a
            row does not have the same number of fields as the header.
            The message includes the line number when relevant, and the
            original exception is chained when there is one.
    """
    try:
        with open(path, encoding="utf-8", newline='') as file:
            reader = csv.reader(file)
            try:
                header = next(reader)
            except StopIteration as error:
                raise CsvLoadError(f"CSV file {path!r} is empty") from error
            if not header: 
                raise CsvLoadError(f"CSV file {path!r} has an empty header")
            rows = []
            for row in reader:
                if not row:
                    continue
                if len(row) != len(header):
                    raise CsvLoadError(f"CSV file {path!r}, line {reader.line_num}: expected {len(header)} fields, got {len(row)}")
                rows.append(row)
    except OSError as error:
        raise CsvLoadError(f"CSV file {path!r} cannot be opened") from error 
    except UnicodeDecodeError as error:
        raise CsvLoadError(f"CSV file {path!r} is not valid UTF-8") from error
    return header, rows