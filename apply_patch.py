
import re
from pathlib import Path

config_path = Path("venv/Lib/site-packages/chromadb/config.py")

if not config_path.exists():
    print(f"Error: {config_path} not found")
    exit(1)

content = config_path.read_text(encoding="utf-8")

# List of prefixes/fields to remove
# These fields cause ConfigError in Pydantic v1 due to Optional typing issues.
prefixes = [
    "chroma_server_", 
    "chroma_client_", 
    "chroma_http_",
    "chroma_segment_cache_policy",
    "chroma_quota_provider_impl",
    "chroma_rate_limiting_provider_impl",
    "chroma_auth_token_transport_header",
    "chroma_otel_granularity",
    "chroma_server_grpc_port"
]
prefix_pattern = "|".join(prefixes)

# Pattern: match lines defining these fields as Optional
pattern = r"(\s+)(" + prefix_pattern + r")[a-z0-9_]*: Optional\[.*\](?: = .*)?"
replacement = ""

new_content = re.sub(pattern, replacement, content)

# Remove usage of chroma_server_nofile
pattern_usage = r'settings\["chroma_server_nofile"\]'
replacement_usage = "None"
new_content = re.sub(pattern_usage, replacement_usage, new_content)

# Remove usage of chroma_segment_cache_policy
pattern_usage2 = r'settings\["chroma_segment_cache_policy"\]'
replacement_usage2 = "None"
new_content = re.sub(pattern_usage2, replacement_usage2, new_content)

if content == new_content:
    print("No additional changes made.")
else:
    print("Applying updated patch (more fields + usages)...")
    config_path.write_text(new_content, encoding="utf-8")
    print("Patch applied successfully.")
