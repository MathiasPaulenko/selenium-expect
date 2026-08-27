# Composition

Composition assertions combine multiple conditions with AND, OR, or NOT logic.

## `to_satisfy_all(*conditions)`

Asserts that **all** conditions pass (AND logic). Each condition is a callable that receives the target and may raise `AssertionError`.

```python
from selenium_expect import expect

expect(element).to_satisfy_all(
    lambda el: expect(el).to_be_visible(),
    lambda el: expect(el).to_have_text("Submit"),
    lambda el: expect(el).to_be_enabled(),
)
```

Each condition is responsible for its own retry/timeout via `expect()`.

## `to_satisfy_any(*conditions)`

Asserts that **at least one** condition passes (OR logic).

```python
expect(element).to_satisfy_any(
    lambda el: expect(el).to_have_text("Active"),
    lambda el: expect(el).to_have_text("Pending"),
)
```

## `to_satisfy_none(*conditions)`

Asserts that **no** condition passes (NOT logic).

```python
expect(element).to_satisfy_none(
    lambda el: expect(el).to_have_text("Error"),
    lambda el: expect(el).to_have_text("Failed"),
)
```

## Negation

All composition methods support negation via `.not_`:

```python
# Assert NOT all pass (at least one fails)
expect(element).not_.to_satisfy_all(
    lambda el: expect(el).to_be_visible(),
    lambda el: expect(el).to_have_text("Hidden"),
)

# Assert NOT any pass (none pass)
expect(element).not_.to_satisfy_any(
    lambda el: expect(el).to_have_text("Error"),
)
```

## Error messages

When a composition fails, the error message includes all individual failures:

```text
Expected composition to_satisfy_all, but got all pass
  Expected: all pass
  Actual:   condition 0: Expected <button> to be visible, but got False
            condition 1: Expected <button> to have text 'Submit', but got 'Cancel'
  Waited:   0ms (2 polls at 0.0s interval)
```

## Custom message

Pass a `message` to `expect()` for composition context:

```python
expect(element, message="Submit button validation").to_satisfy_all(
    lambda el: expect(el).to_be_visible(),
    lambda el: expect(el).to_have_text("Submit"),
)
```

## More examples

### Validating a form field with multiple conditions

```python
def test_email_field(driver):
    email = driver.find_element(By.ID, "email")

    expect(email).to_satisfy_all(
        lambda el: expect(el).to_be_visible(),
        lambda el: expect(el).to_be_enabled(),
        lambda el: expect(el).to_have_attribute("type", "email"),
        lambda el: expect(el).to_have_attribute("placeholder", "Enter your email"),
        lambda el: expect(el).to_have_value(""),
    )
```

### Checking for one of several valid states

```python
def test_order_status(driver):
    status = driver.find_element(By.ID, "order-status")

    # Status should be one of these values
    expect(status).to_satisfy_any(
        lambda el: expect(el).to_have_text("Processing"),
        lambda el: expect(el).to_have_text("Shipped"),
        lambda el: expect(el).to_have_text("Delivered"),
    )
```

### Ensuring none of the error states are present

```python
def test_no_errors(driver):
    expect(driver.find_element(By.ID, "notification")).to_satisfy_none(
        lambda el: expect(el).to_have_text("Error"),
        lambda el: expect(el).to_have_text("Failed"),
        lambda el: expect(el).to_have_text("Timeout"),
    )
```

### Using with locator-based expect

```python
expect(driver, by=By.ID, value="submit-btn").to_satisfy_all(
    lambda el: expect(el).to_be_visible(),
    lambda el: expect(el).to_be_enabled(),
    lambda el: expect(el).to_have_text("Submit"),
)
```
