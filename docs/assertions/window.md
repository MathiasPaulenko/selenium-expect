# Window assertions

Window assertions are available via `expect(driver)` (inherited by `ExpectDriver`). They operate on `driver.get_window_position()`, `driver.get_window_size()`, and `driver.get_window_rect()`.

## Position

### `to_have_position(x, y)`

Asserts that the window position matches `(x, y)`.

**Selenium API**: `driver.get_window_position()`

**Parameters**:

- `x` (`int`): Expected X coordinate.
- `y` (`int`): Expected Y coordinate.

**Example**:

```python
expect(driver).to_have_position(0, 0)
```

**Negation**:

```python
expect(driver).not_.to_have_position(100, 100)
```

## Size

### `to_have_size(width, height)`

Asserts that the window size matches `(width, height)`.

**Selenium API**: `driver.get_window_size()`

**Parameters**:

- `width` (`int`): Expected width in pixels.
- `height` (`int`): Expected height in pixels.

**Example**:

```python
expect(driver).to_have_size(1280, 800)
```

## Rect

### `to_have_rect(x, y, width, height)`

Asserts that the window rect matches all four values.

**Selenium API**: `driver.get_window_rect()`

**Parameters**:

- `x` (`int`): Expected X coordinate.
- `y` (`int`): Expected Y coordinate.
- `width` (`int`): Expected width.
- `height` (`int`): Expected height.

**Example**:

```python
expect(driver).to_have_rect(0, 0, 1280, 800)
```

## Tips and common patterns

### Setting and verifying window size

```python
# Set the window size
driver.set_window_size(1920, 1080)

# Verify it was set correctly
expect(driver).to_have_size(1920, 1080)
```

### Setting and verifying window position

```python
# Move the window to the top-left corner
driver.set_window_position(0, 0)

# Verify the position
expect(driver).to_have_position(0, 0)
```

### Verifying full window rect

```python
# Set position and size together
driver.set_window_rect(100, 100, 1280, 720)

# Verify all four values
expect(driver).to_have_rect(100, 100, 1280, 720)
```

### Negation

```python
# Window is NOT at position (0, 0)
expect(driver).not_.to_have_position(0, 0)

# Window is NOT 800x600
expect(driver).not_.to_have_size(800, 600)
```

### Using with window management

```python
# After maximizing the window
driver.maximize_window()

# Verify the window is no longer small
expect(driver).not_.to_have_size(800, 600)

# After switching to a new window
driver.switch_to.window(driver.window_handles[1])

# Verify the new window's size
expect(driver).to_have_size(1024, 768)
```
