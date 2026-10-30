# Case Study 91: Registration Record Checker

## What it does

This program checks registration details stored as text. It splits each line into fields and reports records that do not follow the expected format.

## Main steps

1. Split a record using the `|` character.
2. Check the registration number, name, date, category, and status.
3. Look for duplicate registration numbers.
4. Print accepted records and error messages.

## Python topics

Strings, `split()`, indexing, lists, tuples, loops, and conditions.

## Run it

```text
python solution.py
```

The program uses sample registration strings. See [output.txt](output.txt) and [flowchart.svg](flowchart.svg).
