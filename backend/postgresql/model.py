"""Database model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, func
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Product(Base):
    """
    Class of create table Product info
    """
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    create_date = Column(DateTime, server_default=func.now())
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    numbers = Column(Integer, default=0)
    status = Column(Boolean, default=False)
    author = Column(String, nullable=False)
    contact = Column(String, nullable=False)

    images = relationship("ImageProduct")
    videos = relationship("ImageProduct")

    __mapper_args__ = {"eager_defaults": True}


class ImageProduct(Base):
    """
    Class of create table Product images
    """
    __tablename__ = "image_product"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(ForeignKey("product.product_id"))
    link = Column(String, unique=True, nullable=False)


class VideoProduct(Base):
    """
    Class of create table Product videos
    """
    __tablename__ = "video_product"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(ForeignKey("product.product_id"))
    link = Column(String, unique=True, nullable=False)
