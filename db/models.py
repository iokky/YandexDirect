from sqlalchemy import Column, Integer, String, DECIMAL, UniqueConstraint
from .db import Base


class YandexDirect(Base):
    __tablename__ = 'yandex_direct_dev'
    __table_args__ = (UniqueConstraint('direct_index', name='yandex_direct_index'),)

    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    date = Column(String)
    campaign = Column(String)
    impressions = Column(Integer)
    clicks = Column(Integer)
    cost = Column(DECIMAL)

    direct_index = Column(String(256))

    def __init__(self, date, campaign, impressions, clicks, cost, direct_index):
        self.date = date
        self.campaign = campaign
        self.impressions = impressions
        self.clicks = clicks
        self.cost = cost
        self.direct_index = direct_index

