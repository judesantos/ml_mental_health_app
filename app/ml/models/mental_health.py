from web.extensions import db
from flask_login import UserMixin


class MentalHealthModel(db.Model, UserMixin):

    """
    This class defines the db model for the CDC data.

    Properties with corresponding columns in the db table:
        'POORHLTH',
        'PHYSHLTH',
        'SDHSTRE1',
        'ADDEPEV3',
        'INCOME3',
        'EDUCA',
        'MARITAL',
        '_STATE',
        'GENHLTH',
        'EMPLOY1',
        'LSATISFY',
        'EMTSUPRT',
        'DECIDE',
        'ALCDAY4',
        'SMOKDAY2',
        'DIFFWALK',
        'PREGNANT',
        'EXEROFT1',
        'SDLONELY',
        'HAVARTH4',
        'CHECKUP1',
        'VETERAN3',
        'MEDCOST1',
        'MARIJAN1',
        'ACEDEPRS',
        'SDHFOOD1',
        'CVDCRHD4',
        'CHOLMED3',
        'ADULT',
        'SDHTRNSP',
        'ASTHNOW',
        'CHCSCNC1',
        'RRCLASS3',
        'SDHBILLS',
        'CHCCOPD3',
        '_URBSTAT',
        'QSTLANG',
        'DIFFALON',
        'DIABETE4',
        'CHOLCHK3',
        'BPMEDS1',
        'DIFFDRES',
        'CVDSTRK3',
        'BPHIGH6',
        'FIREARM5',
        'CHCKDNY2',
        'SDHEMPLY',
        'SDHUTILS',
        'CDDISCU1',
        'CDHOUS1',
        'CIMEMLO1',
        'CHCOCNC1',
        'FOODSTMP',
        'USENOW3',
        'SEX',
        'CDSOCIA1',
    """

    __tablename__ = 'cdc_data'

    # General Health Section listed according to its unique id:

    poorhlth = db.Column('POORHLTH', db.Integer, unique=True, nullable=False)
    physhlth = db.Column('PHYSHLTH', db.Integer, unique=True, nullable=False)
    genhlth  = db.Column('GENHLTH', db.Integer, unique=True, nullable=False)
    diffwalk = db.Column('DIFFWALK', db.Integer, unique=True, nullable=False)
    diffalon = db.Column('DIFFALON', db.Integer, unique=True, nullable=False)
    checkup1 = db.Column('CHECKUP1', db.Integer, unique=True, nullable=False)
    diffdres = db.Column('DIFFDRES', db.Integer, unique=True, nullable=False)

    # Mental Health Section:

    addepev3 = db.Column('ADDEPEV3', db.Integer, unique=True, nullable=False)
    acedeprs = db.Column('ACEDEPRS', db.Integer, unique=True, nullable=False)
    sdlonely = db.Column('SDLONELY', db.Integer, unique=True, nullable=False)
    lsatisfy = db.Column('LSATISFY', db.Integer, unique=True, nullable=False)
    emtsuprt = db.Column('EMTSUPRT', db.Integer, unique=True, nullable=False)
    decide   = db.Column('DECIDE', db.Integer, unique=True, nullable=False)
    cdsocia1 = db.Column('CDSOCIA1', db.Integer, unique=True, nullable=False)
    cddiscu1 = db.Column('CDDISCU1', db.Integer, unique=True, nullable=False)
    cimemlo1 = db.Column('CIMEMLO1', db.Integer, unique=True, nullable=False)

    # Lifestyle and Habits Section:

    smokday2 = db.Column('SMOKDAY2', db.Integer, unique=True, nullable=False)
    alcday4  = db.Column('ALCDAY4', db.Integer, unique=True, nullable=False)
    marijan1 = db.Column('MARIJAN1', db.Integer, unique=True, nullable=False)
    exeroft1 = db.Column('EXEROFT1', db.Integer, unique=True, nullable=False)
    usenow3  = db.Column('USENOW3', db.Integer, unique=True, nullable=False)
    firearm5 = db.Column('FIREARM5', db.Integer, unique=True, nullable=False)

    # Socioeconomic Factors Section:

    income3  = db.Column('INCOME3', db.Integer, unique=True, nullable=False)
    educa    = db.Column('EDUCA', db.Integer, unique=True, nullable=False)
    employ1  = db.Column('EMPLOY1', db.Integer, unique=True, nullable=False)
    sex      = db.Column('SEX', db.Integer, unique=True, nullable=False)
    marital  = db.Column('MARITAL', db.Integer, unique=True, nullable=False)
    adult    = db.Column('ADULT', db.Integer, unique=True, nullable=False)
    rrclass3 = db.Column('RRCLASS3', db.Integer, unique=True, nullable=False)
    qstlang  = db.Column('QSTLANG', db.Integer, unique=True, nullable=False)
    _state   = db.Column('_STATE', db.Integer, unique=True, nullable=False)
    veteran3 = db.Column('VETERAN3', db.Integer, unique=True, nullable=False)
    medcost1 = db.Column('MEDCOST1', db.Integer, unique=True, nullable=False)
    sdhbills = db.Column('SDHBILLS', db.Integer, unique=True, nullable=False)
    sdhemply = db.Column('SDHEMPLY', db.Integer, unique=True, nullable=False)
    sdhfood1 = db.Column('SDHFOOD1', db.Integer, unique=True, nullable=False)
    sdhstre1 = db.Column('SDHSTRE1', db.Integer, unique=True, nullable=False)
    sdhutils = db.Column('SDHUTILS', db.Integer, unique=True, nullable=False)
    sdhtrnsp = db.Column('SDHTRNSP', db.Integer, unique=True, nullable=False)
    cdhous1  = db.Column('CDHOUS1', db.Integer, unique=True, nullable=False)
    foodstmp = db.Column('FOODSTMP', db.Integer, unique=True, nullable=False)

    # Chronic Conditions and Medical History Section:

    pregnant = db.Column('PREGNANT', db.Integer, unique=True, nullable=False)
    asthnow  = db.Column('ASTHNOW', db.Integer, unique=True, nullable=False)
    havarth4 = db.Column('HAVARTH4', db.Integer, unique=True, nullable=False)
    chcscnc1 = db.Column('CHCSCNC1', db.Integer, unique=True, nullable=False)
    chcocnc1 = db.Column('CHCOCNC1', db.Integer, unique=True, nullable=False)
    diabete4 = db.Column('DIABETE4', db.Integer, unique=True, nullable=False)
    chccopd3 = db.Column('CHCCOPD3', db.Integer, unique=True, nullable=False)
    cholchk3 = db.Column('CHOLCHK3', db.Integer, unique=True, nullable=False)
    bpmeds1  = db.Column('BPMEDS1', db.Integer, unique=True, nullable=False)
    bphigh6  = db.Column('BPHIGH6', db.Integer, unique=True, nullable=False)
    cvdstrk3 = db.Column('CVDSTRK3', db.Integer, unique=True, nullable=False)
    cvdcrhd4 = db.Column('CVDCRHD4', db.Integer, unique=True, nullable=False)
    chckdny2 = db.Column('CHCKDNY2', db.Integer, unique=True, nullable=False)
    cholmed3 = db.Column('CHOLMED3', db.Integer, unique=True, nullable=False)


