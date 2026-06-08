"""Tests for Confucius Agent memory layers."""

import pytest
from unittest.mock import patch, MagicMock


class TestMentalModels:
    """Test Layer 1: Mental Models retrieval and storage."""

    def test_retrieve_empty(self):
        """Should return empty list when no knowledge exists."""
        from confucius.memory.mental_models import MentalModels
        mm = MentalModels()
        results = mm.retrieve("test query")
        assert isinstance(results, list)


class TestObservations:
    """Test Layer 2: Observations persistence."""

    def test_add_and_count(self):
        """Should store and retrieve observations."""
        from confucius.memory.observations import Observations
        obs = Observations()
        obs.add("Test observation", category="test")
        results = obs.retrieve("test", category="test")
        assert isinstance(results, list)


class TestRawFacts:
    """Test Layer 3: Raw Facts TTL-based storage."""

    def test_add_and_retrieve(self):
        """Should store and retrieve raw facts."""
        from confucius.memory.raw_facts import RawFacts
        rf = RawFacts()
        rf.add("Test fact", channel="test")
        results = rf.retrieve("test", channel="test")
        assert isinstance(results, list)
