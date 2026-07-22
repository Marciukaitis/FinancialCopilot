"""Memoria conversacional de LangGraph (checkpointer in-memory)."""

from langgraph.checkpoint.memory import MemorySaver

# Instancia compartida: mantiene el historial por thread_id mientras corre el proceso.
memory_saver = MemorySaver()
