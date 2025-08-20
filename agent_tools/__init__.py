"""
Agent Tools - Simple library for Snowflake Intelligence agent tools

Focus: Local development + easy Snowflake deployment
No over-engineering, just what you need to build and deploy tools.
"""

from .snowflake_connection import SnowflakeConnection, ConnectionConfig

__version__ = "0.1.0"

__all__ = ["SnowflakeConnection", "ConnectionConfig"]