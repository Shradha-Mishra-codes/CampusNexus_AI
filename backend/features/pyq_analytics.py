"""
PYQ (Previous Year Questions) Analytics
Analyzes patterns, topics, and difficulty in question papers
"""
from typing import List, Dict, Any
from collections import Counter
import re
from backend.llm.ollama_client import get_ollama_client


class PYQAnalytics:
    """Analyzes Previous Year Questions"""
    
    def __init__(self):
        self.ollama_client = get_ollama_client()
    
    def analyze_questions(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze PYQ documents for patterns and insights
        
        Args:
            documents: List of document chunks from PYQs
            
        Returns:
            Analytics result with patterns and statistics
        """
        try:
            # Extract questions from documents
            all_text = " ".join([doc.get("text", "") for doc in documents])
            questions = self._extract_questions(all_text)
            
            # Analyze topics using LLM
            topic_analysis = self._analyze_topics(questions)
            
            # Calculate statistics
            year_distribution = self._extract_year_distribution(documents)
            difficulty_distribution = self._estimate_difficulty(questions)
            
            # Identify patterns
            patterns = self._identify_patterns(topic_analysis, year_distribution)
            
            return {
                "total_questions": len(questions),
                "patterns": patterns,
                "topic_distribution": topic_analysis,
                "difficulty_distribution": difficulty_distribution,
                "year_wise_trends": year_distribution
            }
            
        except Exception as e:
            raise RuntimeError(f"PYQ analysis failed: {str(e)}")
    
    def _extract_questions(self, text: str) -> List[str]:
        """Extract individual questions from text"""
        # Simple heuristic: split by question numbers or question marks
        questions = []
        
        # Pattern for numbered questions (e.g., "1.", "Q1:", etc.)
        question_patterns = [
            r'\n\s*\d+\.\s+',
            r'\n\s*Q\d+[\.:]\s+',
            r'\n\s*Question\s+\d+[\.:]\s+'
        ]
        
        parts = [text]
        for pattern in question_patterns:
            new_parts = []
            for part in parts:
                new_parts.extend(re.split(pattern, part))
            parts = new_parts
        
        # Filter and clean
        for part in parts:
            part = part.strip()
            if len(part) > 20:  # Minimum length for a question
                questions.append(part[:500])  # Limit length
        
        return questions if questions else [text[:1000]]
    
    def _analyze_topics(self, questions: List[str]) -> Dict[str, int]:
        """Analyze topics in questions using LLM"""
        # Sample questions if too many
        sample_questions = questions[:20] if len(questions) > 20 else questions
        
        questions_text = "\n".join([f"{i+1}. {q[:200]}" for i, q in enumerate(sample_questions)])
        
        prompt = f"""Analyze these exam questions and identify the main topics covered.
List ONLY the topic names, one per line, no explanations.

QUESTIONS:
{questions_text}

TOPICS (one per line):"""
        
        try:
            response = self.ollama_client.generate(prompt)
            
            # Parse topics from response
            topics = []
            for line in response.split('\n'):
                line = line.strip()
                # Remove numbered list markers
                line = re.sub(r'^\d+[\.\)]\s*', '', line)
                line = re.sub(r'^[-*]\s*', '', line)
                if line and len(line) > 3:
                    topics.append(line[:50])  # Limit topic name length
            
            # Count topic frequency
            topic_counts = Counter(topics)
            return dict(topic_counts.most_common(10))
            
        except Exception as e:
            print(f"Topic analysis failed: {str(e)}")
            return {"General": len(questions)}
    
    def _extract_year_distribution(self, documents: List[Dict[str, Any]]) -> Dict[str, int]:
        """Extract year information from document metadata"""
        year_pattern = r'20\d{2}|19\d{2}'
        year_counts = Counter()
        
        for doc in documents:
            metadata = doc.get("metadata", {})
            filename = metadata.get("filename", "")
            
            # Find years in filename
            years = re.findall(year_pattern, filename)
            for year in years:
                year_counts[year] += 1
        
        return dict(year_counts.most_common())
    
    def _estimate_difficulty(self, questions: List[str]) -> Dict[str, int]:
        """Estimate difficulty distribution"""
        difficulty_counts = {"Easy": 0, "Medium": 0, "Hard": 0}
        
        for question in questions:
            # Simple heuristic based on length and complexity keywords
            word_count = len(question.split())
            complexity_keywords = ['explain', 'analyze', 'evaluate', 'compare', 'derive', 'prove']
            
            has_complexity = any(keyword in question.lower() for keyword in complexity_keywords)
            
            if word_count < 20 and not has_complexity:
                difficulty_counts["Easy"] += 1
            elif word_count > 50 or has_complexity:
                difficulty_counts["Hard"] += 1
            else:
                difficulty_counts["Medium"] += 1
        
        return difficulty_counts
    
    def _identify_patterns(
        self,
        topic_distribution: Dict[str, int],
        year_distribution: Dict[str, int]
    ) -> List[Dict[str, Any]]:
        """Identify important patterns"""
        patterns = []
        
        # Pattern: Most frequent topics
        for topic, frequency in list(topic_distribution.items())[:5]:
            years = list(year_distribution.keys())
            patterns.append({
                "topic": topic,
                "frequency": frequency,
                "years": [int(y) for y in years[:3]] if years else [],
                "difficulty": "Medium",  # Simplified
                "importance_score": min(1.0, frequency / 10.0)
            })
        
        return patterns


def get_pyq_analytics() -> PYQAnalytics:
    """Get PYQAnalytics instance"""
    return PYQAnalytics()
