from pymilvus import connections, Collection
from src.app.config import settings


def preview(limit=5):
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

    results = collection.query(
        expr="id >= 0",
        output_fields=["text"],
        limit=limit,
    )

    print(f"\n🔎 Showing {len(results)} stored chunks:\n")
    for i, r in enumerate(results, start=1):
        print(f"[CHUNK {i}]")
        print(r["text"])
        print("-" * 60)


if __name__ == "__main__":
    preview()
