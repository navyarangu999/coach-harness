"""Creates a batch of buggy practice tasks under tasks/.

Run once from the project root:  python make_tasks.py

Each task is a folder with a <name>.py (containing one planted bug) and a
test_<name>.py (whose tests fail until the bug is fixed). Existing folders are
left untouched, so it is safe to re-run.
"""
from pathlib import Path

TASKS = {
    # 1. Off-by-one in a range.
    "countdown": {
        "code": '''\
def countdown(n):
    """Return a list from n down to 1 (inclusive)."""
    # BUG: range stops one short, so 1 is missing
    return list(range(n, 1, -1))
''',
        "test": '''\
from countdown import countdown


def test_countdown():
    assert countdown(5) == [5, 4, 3, 2, 1]


def test_countdown_one():
    assert countdown(1) == [1]
''',
    },

    # 2. Wrong comparison operator.
    "max_finder": {
        "code": '''\
def find_max(numbers):
    """Return the largest number in a non-empty list."""
    best = numbers[0]
    for n in numbers:
        # BUG: wrong comparison keeps the smallest instead of the largest
        if n < best:
            best = n
    return best
''',
        "test": '''\
from max_finder import find_max


def test_find_max():
    assert find_max([3, 7, 2, 9, 4]) == 9


def test_find_max_negatives():
    assert find_max([-5, -2, -9]) == -2
''',
    },

    # 3. Mutable default argument.
    "accumulator": {
        "code": '''\
def add_item(item, basket=[]):
    """Add item to a basket and return it. Each call should start fresh."""
    # BUG: shared mutable default keeps items between calls
    basket.append(item)
    return basket
''',
        "test": '''\
from accumulator import add_item


def test_fresh_basket_each_call():
    assert add_item("a") == ["a"]
    assert add_item("b") == ["b"]
''',
    },

    # 4. Integer division where float is expected.
    "grades": {
        "code": '''\
def percentage(scored, total):
    """Return the percentage score as a float."""
    # BUG: integer division truncates the decimal part
    return scored // total * 100
''',
        "test": '''\
from grades import percentage


def test_percentage():
    assert percentage(1, 8) == 12.5


def test_percentage_half():
    assert percentage(1, 2) == 50.0
''',
    },

    # 5. Off-by-one in a slice.
    "last_n": {
        "code": '''\
def last_n(items, n):
    """Return the last n items of a list, in order."""
    # BUG: this returns the first n items, not the last n
    return items[:n]
''',
        "test": '''\
from last_n import last_n


def test_last_n():
    assert last_n([1, 2, 3, 4, 5], 2) == [4, 5]


def test_last_n_all():
    assert last_n([1, 2, 3], 3) == [1, 2, 3]
''',
    },

    # 6. Wrong boundary in a conditional.
    "fizzbuzz": {
        "code": '''\
def fizzbuzz(n):
    """Classic FizzBuzz for a single number."""
    # BUG: checks 3 and 5 before 15, so multiples of both never say FizzBuzz
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    if n % 15 == 0:
        return "FizzBuzz"
    return str(n)
''',
        "test": '''\
from fizzbuzz import fizzbuzz


def test_fizz():
    assert fizzbuzz(9) == "Fizz"


def test_buzz():
    assert fizzbuzz(10) == "Buzz"


def test_fizzbuzz():
    assert fizzbuzz(15) == "FizzBuzz"
''',
    },

    # 7. String method misuse.
    "titlecase": {
        "code": '''\
def capitalize_words(sentence):
    """Capitalize the first letter of each word."""
    # BUG: capitalize() only capitalizes the first word of the whole string
    return sentence.capitalize()
''',
        "test": '''\
from titlecase import capitalize_words


def test_capitalize_words():
    assert capitalize_words("hello there world") == "Hello There World"
''',
    },

    # 8. Incorrect accumulator start value.
    "product": {
        "code": '''\
def product(numbers):
    """Return the product of all numbers in a list."""
    # BUG: starting at 0 makes every product 0
    result = 0
    for n in numbers:
        result *= n
    return result
''',
        "test": '''\
from product import product


def test_product():
    assert product([2, 3, 4]) == 24


def test_product_single():
    assert product([7]) == 7
''',
    },

    # 9. Missing strip / wrong whitespace handling.
    "word_count": {
        "code": '''\
def word_count(text):
    """Count the words in a string, ignoring extra spaces."""
    # BUG: splitting on " " creates empty strings from double spaces
    return len(text.split(" "))
''',
        "test": '''\
from word_count import word_count


def test_simple():
    assert word_count("one two three") == 3


def test_extra_spaces():
    assert word_count("one  two   three") == 3
''',
    },

    # 10. Logic error in a recursive base case.
    "factorial": {
        "code": '''\
def factorial(n):
    """Return n! for n >= 0."""
    # BUG: base case is wrong, so factorial(0) returns 0 instead of 1
    if n == 0:
        return 0
    return n * factorial(n - 1)
''',
        "test": '''\
from factorial import factorial


def test_factorial():
    assert factorial(5) == 120


def test_factorial_zero():
    assert factorial(0) == 1
''',
    },
}


def main():
    tasks_root = Path("tasks")
    tasks_root.mkdir(exist_ok=True)

    created, skipped = 0, 0
    for name, files in TASKS.items():
        folder = tasks_root / name
        if folder.exists():
            skipped += 1
            continue
        folder.mkdir()
        (folder / f"{name}.py").write_text(files["code"], encoding="utf-8")
        (folder / f"test_{name}.py").write_text(files["test"], encoding="utf-8")
        created += 1
        print(f"created tasks/{name}/")

    print(f"\nDone. {created} created, {skipped} already existed.")


if __name__ == "__main__":
    main()