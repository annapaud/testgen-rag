import os
import sys
import argparse
from llama_index.core import VectorStoreIndex, Settings, PromptTemplate
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Pre-defined feature presets (easily expandable)
PRESET_FEATURES = {
    "1": ("User Password & Security Policy", "Identify test scenarios and cases for user password rules and complexity requirements."),
    "2": ("Account Lockout & Recovery", "Identify test scenarios and cases for failed login attempts, account lockout timers, and password resets."),
    "3": ("Full Authentication Suite", "Identify all test scenarios and cases for complete user authentication, security rules, and account lockout handling.")
}

def read_prompt(filepath: str) -> PromptTemplate:
    with open(filepath, "r") as f:
        return PromptTemplate(f.read())

def select_feature_query() -> str:
    print("\n=========================================")
    print("      TESTGEN-RAG FEATURE SELECTOR      ")
    print("=========================================")
    for key, (name, _) in PRESET_FEATURES.items():
        print(f"  [{key}] {name}")
    print("  [4] Custom Query (Enter your own feature focus)")
    print("-----------------------------------------")
    
    choice = input("Select a feature choice [1-4] (default: 3): ").strip()
    
    if choice in PRESET_FEATURES:
        return PRESET_FEATURES[choice][1]
    elif choice == "4":
        custom = input("Enter custom feature query: ").strip()
        return custom if custom else PRESET_FEATURES["3"][1]
    else:
        print("-> Using default: Full Authentication Suite")
        return PRESET_FEATURES["3"][1]

def run_pipeline(user_query: str):
    Settings.embed_model = OllamaEmbedding(
        model_name="nomic-embed-text",
        base_url=OLLAMA_HOST,
        request_timeout=300.0
    )
    Settings.llm = Ollama(
        model="llama3",
        base_url=OLLAMA_HOST,
        request_timeout=600.0
    )

    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    vector_store = QdrantVectorStore(client=client, collection_name="requirements")
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    scenario_prompt = read_prompt("prompts/scenario_prompt.txt")
    detailed_prompt = read_prompt("prompts/detailed_case_prompt.txt")

    print(f"\n[Stage 1/2]: Identifying Scenarios for query: '{user_query}'...")
    scenario_engine = index.as_query_engine(
        similarity_top_k=3,
        text_qa_template=scenario_prompt,
        response_mode="compact"
    )
    scenarios_response = str(scenario_engine.query(user_query))
    print("\n--- TEST SCENARIOS IDENTIFIED ---")
    print(scenarios_response)

    print("\n[Stage 2/2]: Expanding Scenarios into Detailed Test Cases...")
    detail_engine = index.as_query_engine(
        similarity_top_k=3,
        text_qa_template=detailed_prompt,
        response_mode="compact"
    )
    detailed_response = str(detail_engine.query(scenarios_response))
    print("\n--- DETAILED STEP-BY-STEP TEST CASES ---")
    print(detailed_response)

    os.makedirs("tests", exist_ok=True)
    with open("tests/scenarios.json", "w") as f:
        f.write(scenarios_response)
    with open("tests/detailed_test_cases.json", "w") as f:
        f.write(detailed_response)
    
    print("\n? Saved scenarios to tests/scenarios.json")
    print("? Saved detailed test cases to tests/detailed_test_cases.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Case Generator RAG Pipeline")
    parser.add_argument("--feature", type=str, help="Specify feature query directly without interactive menu")
    args = parser.parse_args()

    selected_query = args.feature if args.feature else select_feature_query()
    run_pipeline(selected_query)
