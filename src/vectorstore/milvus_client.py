from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility,
)

from src.app.config import settings


class MilvusClient:
    def __init__(self):
        self.collection_name = settings.MILVUS_COLLECTION
        self._connect()
        self._ensure_collection()

    # -------------------------------------------------
    # Connect to Milvus
    # -------------------------------------------------
    def _connect(self):
        connections.connect(
            alias="default",
            uri=settings.MILVUS_URI,
            token=settings.MILVUS_TOKEN,
        )

    # -------------------------------------------------
    # Create collection if not exists
    # -------------------------------------------------
    def _ensure_collection(self):
        if utility.has_collection(self.collection_name):
            self.collection = Collection(
                name=self.collection_name,
                using="default",
            )
            return

        fields = [
            FieldSchema(
                name="id",
                dtype=DataType.INT64,
                is_primary=True,
                auto_id=True,
            ),
            FieldSchema(
                name="embedding",
                dtype=DataType.FLOAT_VECTOR,
                dim=768,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=8192,
            ),
            FieldSchema(
                name="document_id",
                dtype=DataType.VARCHAR,
                max_length=128,
            ),
            FieldSchema(
                name="document_name",
                dtype=DataType.VARCHAR,
                max_length=256,
            ),
        ]

        schema = CollectionSchema(
            fields=fields,
            description="Agentic RAG (overwrite-mode, single document)",
        )

        self.collection = Collection(
            name=self.collection_name,
            schema=schema,
            using="default",
        )

        index_params = {
            "index_type": "HNSW",
            "metric_type": "COSINE",
            "params": {"efConstruction": 64, "M": 8},
        }

        self.collection.create_index(
            field_name="embedding",
            index_params=index_params,
        )

    # -------------------------------------------------
    # 🔥 OVERWRITE MODE: reset collection
    # -------------------------------------------------
    def reset_collection(self):
        """
        Drop old document data and recreate collection.
        """
        if utility.has_collection(self.collection_name):
            utility.drop_collection(self.collection_name)

        self._ensure_collection()

    # -------------------------------------------------
    # Insert new document
    # -------------------------------------------------
    def insert(
        self,
        embeddings: list[list[float]],
        texts: list[str],
        document_id: str,
        document_name: str,
    ):
        if len(embeddings) != len(texts):
            raise ValueError("Embeddings and texts length mismatch")

        n = len(texts)

        self.collection.insert(
            [
                embeddings,
                texts,
                [document_id] * n,
                [document_name] * n,
            ]
        )

        self.collection.flush()

    # -------------------------------------------------
    # Search (no filtering needed in overwrite mode)
    # -------------------------------------------------
    def search(
        self,
        query_embedding: list[float],
        top_k: int,
    ):
        self.collection.load()

        results = self.collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param={"metric_type": "COSINE", "params": {"ef": 64}},
            limit=top_k,
            output_fields=["text", "document_name"],
        )

        matches = []
        for hit in results[0]:
            matches.append(
                {
                    "text": hit.entity.get("text"),
                    "score": hit.score,
                    "document": hit.entity.get("document_name"),
                }
            )

        return matches
