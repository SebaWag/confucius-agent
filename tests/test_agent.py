"""Tests for Confucius Agent."""

import pytest
from unittest.mock import patch


class TestAgent:
    """Test the main Confucius Agent."""

    def test_agent_initialization(self):
        """Agent should initialize with default system prompt."""
        from confucius.agent import ConfuciusAgent
        agent = ConfuciusAgent()
        assert agent.system_prompt is not None
        assert "Mental Models" in agent.system_prompt
        assert "Qwen Cloud" in agent.system_prompt

    def test_agent_reset(self):
        """Reset should clear conversation but keep memory."""
        from confucius.agent import ConfuciusAgent
        agent = ConfuciusAgent()
        agent.conversation_history.append({"role": "user", "content": "test"})
        agent.reset_conversation()
        assert len(agent.conversation_history) == 1  # Only system prompt


class TestRetrievalPipeline:
    """Test the memory orchestration pipeline."""

    def test_pipeline_initialization(self):
        """Pipeline should initialize all 3 tiers."""
        from confucius.memory.retrieval_pipeline import RetrievalPipeline
        pipeline = RetrievalPipeline()
        assert pipeline.mental_models is not None
        assert pipeline.observations is not None
        assert pipeline.raw_facts is not None

    def test_query_all_tiers(self):
        """Query should return results from all 3 tiers."""
        from confucius.memory.retrieval_pipeline import RetrievalPipeline
        pipeline = RetrievalPipeline()
        results = pipeline.query("test query")
        assert "context" in results
        assert "tiers_used" in results
        assert "stats" in results
        assert "formatted_context" in results
