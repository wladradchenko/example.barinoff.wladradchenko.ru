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
        yield self.Auction()

    def sql_constructor(self):
        """
        SQL Constructor
        :return: generator from sql
        """
        return (f"create table if not exists {table.__tablename__} {table.__columns__} engine = {table.__engine__} {table.__partition__} {table.__order__};" for table in self.tables)

    class Auction:
        """
        Class of create table Auction as Meta
        """
        def __init__(self) -> None:
            self.__tablename__ = "auction"
            self.__columns__ = "(" \
                                  "date         DateTime," \
                                  "product_id   UInt32," \
                                  "price        UInt32," \
                                  "login        String," \
                                  "message      String," \
                                  "email        String," \
                                  "phone        UInt32," \
                               ")"
            self.__engine__ = "ReplacingMergeTree()"
            self.__partition__ = "partition by toStartOfHour(date)"
            self.__order__ = "order by (product_id, login, email, phone)"
