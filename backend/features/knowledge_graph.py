"""
Knowledge Graph Generation
Extracts entities and relationships from documents
"""
from typing import List, Dict, Any
import networkx as nx
from backend.llm.ollama_client import get_ollama_client
import re


class KnowledgeGraph:
    """Generates knowledge graphs from documents"""
    
    def __init__(self):
        self.ollama_client = get_ollama_client()
        self.graph = nx.DiGraph()
    
    def generate_graph(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate knowledge graph from documents
        
        Args:
            documents: List of document chunks
            
        Returns:
            Graph structure with nodes and edges
        """
        try:
            # Sample documents if too many
            sample_docs = documents[:15] if len(documents) > 15 else documents
            
            # Extract entities and relationships
            for doc in sample_docs:
                text = doc.get("text", "")
                if len(text) > 100:
                    entities_and_relations = self._extract_entities_relationships(text[:1000])
                    self._add_to_graph(entities_and_relations)
            
            # Convert to serializable format
            nodes = []
            for node_id in self.graph.nodes():
                node_data = self.graph.nodes[node_id]
                nodes.append({
                    "id": node_id,
                    "label": node_id,
                    "type": node_data.get("type", "concept"),
                    "properties": {}
                })
            
            edges = []
            for source, target, edge_data in self.graph.edges(data=True):
                edges.append({
                    "source": source,
                    "target": target,
                    "relationship": edge_data.get("relationship", "related_to"),
                    "weight": edge_data.get("weight", 1.0)
                })
            
            # Calculate statistics
            statistics = {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "density": nx.density(self.graph) if len(nodes) > 0 else 0
            }
            
            return {
                "nodes": nodes,
                "edges": edges,
                "statistics": statistics
            }
            
        except Exception as e:
            raise RuntimeError(f"Knowledge graph generation failed: {str(e)}")
    
    def _extract_entities_relationships(self, text: str) -> List[Dict[str, Any]]:
        """Extract entities and relationships using LLM"""
        prompt = f"""Extract key concepts and their relationships from this text.
Format: Entity1 -> Relationship -> Entity2

TEXT:
{text}

RELATIONSHIPS (format: Entity1 -> Relationship -> Entity2):"""
        
        try:
            response = self.ollama_client.generate(prompt)
            
            # Parse relationships
            relationships = []
            for line in response.split('\n'):
                line = line.strip()
                if '->' in line:
                    # Parse format: Entity1 -> Relationship -> Entity2
                    parts = [p.strip() for p in line.split('->')]
                    if len(parts) >= 3:
                        relationships.append({
                            "entity1": parts[0][:50],
                            "relationship": parts[1][:30],
                            "entity2": parts[2][:50]
                        })
                    elif len(parts) == 2:
                        # Format: Entity1 -> Entity2 (default relationship)
                        relationships.append({
                            "entity1": parts[0][:50],
                            "relationship": "related_to",
                            "entity2": parts[1][:50]
                        })
            
            return relationships
            
        except Exception as e:
            print(f"Entity extraction failed: {str(e)}")
            return []
    
    def _add_to_graph(self, relationships: List[Dict[str, Any]]):
        """Add extracted relationships to the graph"""
        for rel in relationships:
            entity1 = rel["entity1"]
            entity2 = rel["entity2"]
            relationship = rel["relationship"]
            
            # Add nodes if they don't exist
            if entity1 and not self.graph.has_node(entity1):
                self.graph.add_node(entity1, type="concept")
            
            if entity2 and not self.graph.has_node(entity2):
                self.graph.add_node(entity2, type="concept")
            
            # Add edge
            if entity1 and entity2:
                if self.graph.has_edge(entity1, entity2):
                    # Increase weight if edge exists
                    self.graph[entity1][entity2]["weight"] += 1
                else:
                    self.graph.add_edge(
                        entity1,
                        entity2,
                        relationship=relationship,
                        weight=1.0
                    )


def get_knowledge_graph() -> KnowledgeGraph:
    """Get KnowledgeGraph instance"""
    return KnowledgeGraph()
