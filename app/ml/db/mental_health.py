from sqlalchemy import Integer, Column
from sqlalchemy.orm import DeclarativeBase
# from config import db


class Base(DeclarativeBase):
    """ Base class for the SqlAlchemy models """
    pass


class MentalHealthDbModel(Base):
    """
    This class defines the db model for the CDC data.

     Attributes:
        id: The unique id for the data.
        POORHLTH: The number of days in poor health.
        PHYSHLTH: The number of days in physical
        GENHLTH: The general health status.


    """

    __tablename__ = 'cdc_data'

    # General Health Section listed according to its unique id:
    id = Column(Integer, primary_key=True)
    POORHLTH = Column(Integer)
    PHYSHLTH = Column(Integer)
    GENHLTH = Column(Integer)
    DIFFWALK = Column(Integer)
    DIFFALON = Column(Integer)
    CHECKUP1 = Column(Integer)
    DIFFDRES = Column(Integer)
    # Mental Health Section:
    ADDEPEV3 = Column(Integer)
    ACEDEPRS = Column(Integer)
    SDLONELY = Column(Integer)
    LSATISFY = Column(Integer)
    EMTSUPRT = Column(Integer)
    DECIDE = Column(Integer)
    CDSOCIA1 = Column(Integer)
    CDDISCU1 = Column(Integer)
    CIMEMLO1 = Column(Integer)
    # Lifestyle and Habits Section:
    SMOKDAY2 = Column(Integer)
    ALCDAY4 = Column(Integer)
    MARIJAN1 = Column(Integer)
    EXEROFT1 = Column(Integer)
    USENOW3 = Column(Integer)
    FIREARM5 = Column(Integer)
    # Socioeconomic Factors Section:
    INCOME3 = Column(Integer)
    EDUCA = Column(Integer)
    EMPLOY1 = Column(Integer)
    SEX = Column(Integer)
    MARITAL = Column(Integer)
    ADULT = Column(Integer)
    RRCLASS3 = Column(Integer)
    QSTLANG = Column(Integer)
    _STATE = Column(Integer)
    VETERAN3 = Column(Integer)
    # Social Determinants of Health Section:
    MEDCOST1 = Column(Integer)
    SDHBILLS = Column(Integer)
    SDHEMPLY = Column(Integer)
    SDHFOOD1 = Column(Integer)
    SDHSTRE1 = Column(Integer)
    SDHUTILS = Column(Integer)
    SDHTRNSP = Column(Integer)
    CDHOUS1 = Column(Integer)
    FOODSTMP = Column(Integer)
    # Chronic Conditions and Medical History Section:
    PREGNANT = Column(Integer)
    ASTHNOW = Column(Integer)
    HAVARTH4 = Column(Integer)
    CHCSCNC1 = Column(Integer)
    CHCOCNC1 = Column(Integer)
    DIABETE4 = Column(Integer)
    CHCCOPD3 = Column(Integer)
    CHOLCHK3 = Column(Integer)
    BPMEDS1 = Column(Integer)
    BPHIGH6 = Column(Integer)
    CVDSTRK3 = Column(Integer)
    CVDCRHD4 = Column(Integer)
    CHCKDNY2 = Column(Integer)
    CHOLMED3 = Column(Integer)
    _MENT14D = Column(Integer)
