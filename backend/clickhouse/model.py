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
        yield self.ShortsVideo()

    def sql_constructor(self):
        """
        SQL Constructor
        :return: generator from sql
        """
        return (f"create table if not exists {table.__tablename__} {table.__columns__} engine = {table.__engine__} {table.__partition__} {table.__order__} {table.__ttl__};" for table in self.tables)

    class ShortsVideo:
        """
        Class of create table Auction as Meta
        """
        def __init__(self) -> None:
            self.__tablename__ = "shorts_video"
            self.__columns__ = "(" \
                                  "date         Date," \
                                  "video_id     String" \
                               ")"
            self.__engine__ = "ReplacingMergeTree()"
            self.__partition__ = ""
            self.__order__ = "ORDER BY video_id"
            self.__ttl__ = "TTL date + INTERVAL 2 WEEK DELETE WHERE toDayOfWeek(date) = 1"
