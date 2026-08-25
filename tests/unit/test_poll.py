"""Unit tests for selenium_expect._poll.PollAssertion and poll()."""

from __future__ import annotations

import pytest

from selenium_expect import expect, poll
from selenium_expect._poll import PollAssertion


class TestPollAssertion:
    def test_to_equal_passes(self) -> None:
        """poll(fn).to_equal(42) passes when fn returns 42."""
        poll(lambda: 42).to_equal(42)

    def test_to_equal_fails(self) -> None:
        """poll(fn).to_equal(99) raises when fn returns 42."""
        with pytest.raises(AssertionError, match="to equal"):
            poll(lambda: 42, timeout=0.5).to_equal(99)

    def test_to_be_truthy_passes(self) -> None:
        """poll(fn).to_be_truthy() passes when fn returns truthy value."""
        poll(lambda: "yes").to_be_truthy()

    def test_to_be_truthy_fails(self) -> None:
        """poll(fn).to_be_truthy() raises when fn returns falsy value."""
        with pytest.raises(AssertionError, match="to be truthy"):
            poll(lambda: "", timeout=0.5).to_be_truthy()

    def test_to_be_falsy_passes(self) -> None:
        """poll(fn).to_be_falsy() passes when fn returns falsy value."""
        poll(lambda: "").to_be_falsy()

    def test_to_be_falsy_fails(self) -> None:
        """poll(fn).to_be_falsy() raises when fn returns truthy value."""
        with pytest.raises(AssertionError, match="to be falsy"):
            poll(lambda: "yes", timeout=0.5).to_be_falsy()

    def test_to_be_none_passes(self) -> None:
        """poll(fn).to_be_none() passes when fn returns None."""
        poll(lambda: None).to_be_none()

    def test_to_be_none_fails(self) -> None:
        """poll(fn).to_be_none() raises when fn returns a value."""
        with pytest.raises(AssertionError, match="to be None"):
            poll(lambda: 42, timeout=0.5).to_be_none()

    def test_to_contain_passes(self) -> None:
        """poll(fn).to_contain('world') passes when fn returns 'hello world'."""
        poll(lambda: "hello world").to_contain("world")

    def test_to_contain_fails(self) -> None:
        """poll(fn).to_contain('missing') raises when fn returns 'hello'."""
        with pytest.raises(AssertionError, match="to contain"):
            poll(lambda: "hello", timeout=0.5).to_contain("missing")

    def test_to_match_passes(self) -> None:
        """poll(fn).to_match(r'\\\\d+') passes when fn returns 'abc123'."""
        poll(lambda: "abc123").to_match(r"\d+")

    def test_to_match_fails(self) -> None:
        """poll(fn).to_match(r'\\\\d+') raises when fn returns 'abc'."""
        with pytest.raises(AssertionError, match="to match"):
            poll(lambda: "abc", timeout=0.5).to_match(r"\d+")

    def test_to_be_greater_than_passes(self) -> None:
        """poll(fn).to_be_greater_than(5) passes when fn returns 10."""
        poll(lambda: 10).to_be_greater_than(5)

    def test_to_be_greater_than_fails(self) -> None:
        """poll(fn).to_be_greater_than(20) raises when fn returns 10."""
        with pytest.raises(AssertionError, match="greater than"):
            poll(lambda: 10, timeout=0.5).to_be_greater_than(20)

    def test_to_be_less_than_passes(self) -> None:
        """poll(fn).to_be_less_than(20) passes when fn returns 10."""
        poll(lambda: 10).to_be_less_than(20)

    def test_to_be_less_than_fails(self) -> None:
        """poll(fn).to_be_less_than(5) raises when fn returns 10."""
        with pytest.raises(AssertionError, match="less than"):
            poll(lambda: 10, timeout=0.5).to_be_less_than(5)

    def test_to_be_in_list_passes(self) -> None:
        """poll(fn).to_be_in_list([1, 2, 3]) passes when fn returns 2."""
        poll(lambda: 2).to_be_in_list([1, 2, 3])

    def test_to_be_in_list_fails(self) -> None:
        """poll(fn).to_be_in_list([1, 2]) raises when fn returns 3."""
        with pytest.raises(AssertionError, match="to be in"):
            poll(lambda: 3, timeout=0.5).to_be_in_list([1, 2])

    def test_to_have_length_passes(self) -> None:
        """poll(fn).to_have_length(3) passes when fn returns [1, 2, 3]."""
        poll(lambda: [1, 2, 3]).to_have_length(3)

    def test_to_have_length_fails(self) -> None:
        """poll(fn).to_have_length(5) raises when fn returns [1, 2, 3]."""
        with pytest.raises(AssertionError, match="to have length"):
            poll(lambda: [1, 2, 3], timeout=0.5).to_have_length(5)


class TestPollRetry:
    def test_retries_until_pass(self) -> None:
        """poll retries until fn returns the expected value."""
        counter = {"n": 0}

        def fn() -> int:
            counter["n"] += 1
            return counter["n"]

        # fn increments each call; by poll 3 it returns 3
        poll(fn, timeout=5, polling=0.01).to_equal(3)
        assert counter["n"] >= 3


class TestExpectPoll:
    def test_expect_poll_returns_poll_assertion(self) -> None:
        """expect.poll(fn) returns a PollAssertion."""
        result = expect.poll(lambda: 42)
        assert isinstance(result, PollAssertion)
        result.to_equal(42)
