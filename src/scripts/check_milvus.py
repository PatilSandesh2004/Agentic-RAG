from pymilvus import connections, Collection
from src.app.config import settings


def check_collection():
    # 🔑 IMPORTANT: bind to alias="default"
    connections.connect(
        alias="default",
        uri=settings.MILVUS_URI,
        token=settings.MILVUS_TOKEN,
    )

    collection = Collection(
        name=settings.MILVUS_COLLECTION,
        using="default",
    )
    collection.load()

    print("✅ Connected to Milvus")
    print("📦 Collection:", collection.name)
    print("📊 Number of entities:", collection.num_entities)
    print("🧱 Schema:", collection.schema)


if __name__ == "__main__":
    check_collection()
