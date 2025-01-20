from pydantic import BaseModel


class MlModelFeatures(BaseModel):
    """
    This class defines the schema for the CDC data model features.
    """
    # General Health Section listed according to its unique id:
    poorhlth: int
    physhlth: int
    genhlth: int
    diffwalk: int
    diffalon: int
    checkup1: int
    diffdres: int
    # Mental Health Section:
    addepev3: int
    acedeprs: int
    sdlonely: int
    lsatisfy: int
    emtsuprt: int
    decide: int
    cdsocia1: int
    cddiscu1: int
    cimemlo1: int
    # Lifestyle and Habits Section:
    smokday2: int
    alcday4: int
    marijan1: int
    exeroft1: int
    usenow3: int
    firearm5: int
    # Socioeconomic Factors Section:
    income3: int
    educa: int
    employ1: int
    sex: int
    marital: int
    adult: int
    rrclass3: int
    qstlang: int
    state: int
    veteran3: int
    # Social Determinants of Health Section:
    medcost1: int
    sdhbills: int
    sdhemply: int
    sdhfood1: int
    sdhstre1: int
    sdhutils: int
    sdhtrnsp: int
    cdhous1: int
    foodstmp: int
    # Chronic Conditions and Medical History Section:
    pregnant: int
    asthnow: int
    havarth4: int
    chcscnc1: int
    chcocnc1: int
    diabete4: int
    chccopd3: int
    cholchk3: int
    bpmeds1: int
    bphigh6: int
    cvdstrk3: int
    cvdcrhd4: int
    chckdny2: int
    cholmed3: int
