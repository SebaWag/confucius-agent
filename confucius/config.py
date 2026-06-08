"""Configuration — works with Qwen Cloud or any OpenAI-compatible API."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuration: use Qwen Cloud for submission, fallback APIs for dev."""
    
    # --- Qwen Cloud (production / submission) ---
    qwen_api_key: Optional[str] = None
    qwen_base_url: str = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    qwen_model: str = "qwen3.7-plus"
    qwen_embedding_model: str = "text-embedding-v3"
    
    # --- Fallback API (development) ---
    # Any OpenAI-compatible API (DeepSeek, Kimi, OpenAI, etc.)
    fallback_api_key: Optional[str] = None
    fallback_base_url: Optional[str] = None
    fallback_model: Optional[str] = None
    
    # Which API to use: "qwen" | "fallback"
    api_mode: str = "fallback"
    
    # --- Databases ---
    chroma_persist_dir: str = "./data/chroma"
    postgres_dsn: str = "postgresql://user:pass@localhost:5432/confucius"
    redis_url: str = "redis://localhost:6379/0"
    
    # --- Memory Tiers ---
    # Mental Models: top-K results from vector search
    mental_models_top_k: int = 5
    mental_models_score_threshold: float = 0.7
    
    # Observations: recency window in days
    observations_recency_days: int = 30
    observations_max_results: int = 10
    
    # Raw Facts: TTL in seconds (default: 1 hour)
    raw_facts_ttl: int = 3600
    raw_facts_max_items: int = 100
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    @property
    def active_api_key(self) -> str:
        if self.api_mode == "qwen" and self.qwen_api_key:
            return self.qwen_api_key
        return self.fallback_api_key or ""
    
    @property
    def active_base_url(self) -> str:
        if self.api_mode == "qwen" and self.qwen_api_key:
            return self.qwen_base_url
        return self.fallback_base_url or "https://api.openai.com/v1"
    
    @property
    def active_model(self) -> str:
        if self.api_mode == "qwen" and self.qwen_api_key:
            return self.qwen_model
        return self.fallback_model or "gpt-4o"


settings = Settings()
