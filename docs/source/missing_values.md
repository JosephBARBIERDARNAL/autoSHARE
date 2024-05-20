# Missing values
***

In [SHARE](https://share-eric.eu/), some responses such as **Don't know** or **Refusal** are categories in themselves. But for most [SHARE](https://share-eric.eu/) data users, these responses are considered as missing values. The method `replace_missing_codes()` is used to replace these responses by `None`.

This method is used according to a **boolean user input** within the app. If the user wants to replace missing codes, the method is called. Otherwise, the method is not called.

## Code
***

::: data.missing_values.MissingValuesManager

# Tests
***

The tests are stored at: `root/tests/test_missing_values.py`

Run the tests with the following command:

```bash
pytest tests/test_missing_values.py
```
