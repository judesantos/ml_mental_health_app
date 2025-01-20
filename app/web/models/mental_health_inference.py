from sqlalchemy import Integer, Column
from web.extensions import db
from web.models.user_inference_log import UserInferenceLog


class MentalHealthDbInferenceModel(db.Model):
    """
    This class defines the db model for the CDC inference data.
    """

    __tablename__ = 'cdc_inference_data'

    # General Health Section listed according to its unique id:
    id = db.Column(db.Integer, primary_key=True)

    # 1. General Health Section

    poorhlth = db.Column('POORHLTH', Integer)
    physhlth = db.Column('PHYSHLTH', Integer)
    genhlth = db.Column('GENHLTH', Integer)
    diffwalk = db.Column('DIFFWALK', Integer)
    diffalon = db.Column('DIFFALON', Integer)
    checkup1 = db.Column('CHECKUP1', Integer)
    diffdres = db.Column('DIFFDRES', Integer)

    # 2. Mental Health Section:

    addepev3 = db.Column('ADDEPEV3', Integer)
    acedeprs = db.Column('ACEDEPRS', Integer)
    sdlonely = db.Column('SDLONELY', Integer)
    lsatisfy = db.Column('LSATISFY', Integer)
    emtsuprt = db.Column('EMTSUPRT', Integer)
    decide = db.Column('DECIDE', Integer)
    cdsocia1 = db.Column('CDSOCIA1', Integer)
    cddiscu1 = db.Column('CDDISCU1', Integer)
    cimemlo1 = db.Column('CIMEMLO1', Integer)

    # 3. Lifestyle and Habits Section:

    smokday2 = db.Column('SMOKDAY2', Integer)
    alcday4 = db.Column('ALCDAY4', Integer)
    marijan1 = db.Column('MARIJAN1', Integer)
    exeroft1 = db.Column('EXEROFT1', Integer)
    usenow3 = db.Column('USENOW3', Integer)
    firearm5 = db.Column('FIREARM5', Integer)

    # 4. Socioeconomic Factors Section:

    income3 = db.Column('INCOME3 ', Integer)
    educa = db.Column('EDUCA', Integer)
    employ1 = db.Column('EMPLOY1', Integer)
    sex = db.Column('SEX', Integer)
    marital = db.Column('MARITAL', Integer)
    adult = db.Column('ADULT', Integer)
    rrclass3 = db.Column('RRCLASS3', Integer)
    qstlang = db.Column('QSTLANG', Integer)
    state = db.Column('_STATE', Integer)
    veteran3 = db.Column('VETERAN3', Integer)

    # 5. Social Determinants of Health Section:

    medcost1 = db.Column('MEDCOST1', Integer)
    sdhbills = db.Column('SDHBILLS', Integer)
    sdhemply = db.Column('SDHEMPLY', Integer)
    sdhfood1 = db.Column('SDHFOOD1', Integer)
    sdhstre1 = db.Column('SDHSTRE1', Integer)
    sdhutils = db.Column('SDHUTILS', Integer)
    sdhtrnsp = db.Column('SDHTRNSP', Integer)
    cdhous1 = db.Column('CDHOUS1', Integer)
    foodstmp = db.Column('FOODSTMP', Integer)

    # 6. Chronic Conditions and Medical History Section:

    pregnant = db.Column('PREGNANT', Integer)
    asthnow = db.Column('ASTHNOW', Integer)
    havarth4 = db.Column('HAVARTH4', Integer)
    chcscnc1 = db.Column('CHCSCNC1', Integer)
    chcocnc1 = db.Column('CHCOCNC1', Integer)
    diabete4 = db.Column('DIABETE4', Integer)
    chccopd3 = db.Column('CHCCOPD3', Integer)
    cholchk3 = db.Column('CHOLCHK3', Integer)
    bpmeds1 = db.Column('BPMEDS1', Integer)
    bphigh6 = db.Column('BPHIGH6', Integer)
    cvdstrk3 = db.Column('CVDSTRK3', Integer)
    cvdcrhd4 = db.Column('CVDCRHD4', Integer)
    chckdny2 = db.Column('CHCKDNY2', Integer)
    cholmed3 = db.Column('CHOLMED3', Integer)
    ment14d = db.Column('_MENT14D', Integer)

    # Relationships
    logs = db.relationship(
        'UserInferenceLog',
        back_populates='inference'
    )
