from studio.knowledge.writer import KnowledgeWriter


def test_knowledge_writer_creates_record():
    writer = KnowledgeWriter()

    record = writer.write(
        title="AI Studio Research",
        content="Testing first knowledge storage",
        tags=["ai", "research"],
    )

    assert record.title == "AI Studio Research"
    assert record.content == "Testing first knowledge storage"
    assert "ai" in record.tags


def test_knowledge_writer_stores_records():
    writer = KnowledgeWriter()

    writer.write(
        title="First Record",
        content="Memory test",
    )

    records = writer.all_records()

    assert len(records) == 1
    assert records[0].title == "First Record"