from studio.core.models import KnowledgeRecord


class KnowledgeWriter:
    """
    Stores validated information into Studio memory.
    """

    def __init__(self):
        self.records = []

    def write(self, title: str, content: str, tags=None) -> KnowledgeRecord:
        """
        Create and store a knowledge record.
        """

        if tags is None:
            tags = []

        record = KnowledgeRecord(
            title=title,
            content=content,
            tags=tags,
        )

        self.records.append(record)

        return record

    def all_records(self):
        """
        Return all stored knowledge.
        """

        return self.records