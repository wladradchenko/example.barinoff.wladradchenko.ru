"""Database model."""


class TableCreator:
    """
    Class to construct table
    """
    def __init__(self) -> None:
        """
        Initialization
        """
        self.tables = self.cls_generator()

    def cls_generator(self):
        """
        Method to return Meta classes to create tables
        :return:
        """
        yield self.Message()

    def sql_constructor(self):
        """
        SQL Constructor
        :return: generator from sql
        """
        return (f"create table if not exists {table.__tablename__} {table.__columns__} engine = {table.__engine__} {table.__partition__} {table.__order__};" for table in self.tables)

    class Message:
        """
        Class of create table Message as Meta
        """
        def __init__(self) -> None:
            self.__tablename__ = "message"
            self.__columns__ = "(" \
                                  "date DateTime," \
                                  "msg  String" \
                               ")"
            self.__engine__ = "ReplacingMergeTree()"
            self.__partition__ = "partition by toStartOfHour(date)"
            self.__order__ = "order by (date, msg)"
