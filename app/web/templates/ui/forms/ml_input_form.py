"""
This module contains the survey form. Used to create the survey form
for the application.

Classes:
    DescriptiveSelectField: A class used to create a select field with
        a 'description' attribute.
    SurveyForm: A class used to create the survey form for the application.
"""

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

from web.templates.ui.ml_features import MLFeaturesMap, MLFeature, create_features


class DescriptiveSelectField(SelectField):
    """
    DescriptiveSelectField is a custom field that extends the SelectField
    class from the WTforms library.

    This field is used to create a select field with descriptive options.

    Attributes:
        choices: A list of tuples containing the field values
            and descriptions.
        description: A description of the field.
    """

    def __init__(self, label='', validators=None, choices=None,
                 description='', default='', **kwargs):

        super(DescriptiveSelectField, self).__init__(
            label=label,
            validators=validators,
            choices=choices,
            default=default,
            **kwargs
        )
        self.id = ''
        self.description = description
        self.selected: tuple = ('', '')


def build_form_item(feature: MLFeature, default='2') -> DescriptiveSelectField:
    """
    Build a form item for the survey form.

    Args:
        feature (MLFeature): The feature to build the form item for.

    Returns:
        DescriptiveSelectField: The form item.
    """

    return DescriptiveSelectField(
        label=feature.label,
        choices=[('', '---')] + feature.get_options(),
        description=feature.question,
        validators=feature.validators,
        default=default
    )


class MlInputForm(FlaskForm):
    """
    Survey Form used to collect user input data for
    the machine learning model prediction.

    Attributes:
        # General Health Section

        poorhlth: The user's general health.
        physhlth: The user's physical health.
        genhlth: The user's general health.
        diffwalk: The user's difficulty walking.
        diffalon: The user's difficulty walking alone.
        checkup1: The user's checkup status.

        # Mental Health Section

        addepev3: The user's mental health.
        acedeprs: The user's depression.
        sdlonely: The user's loneliness.
        lsatisfy: The user's life satisfaction.
        emtsuprt: The user's emotional support.
        decide: The user's decision making.
        cdsocia1: The user's socializing.

        # Lifestyle and Habits Section

        smokday2: The user's smoking habits.
        alcday4: The user's alcohol consumption.
        marijan1: The user's marijuana consumption.
        exeroft1: The user's exercise habits.
        usenow3: The user's drug use.

        # Socioeconomic Factors Section

        income3: The user's income status.
        educa: The user's education status.
        employ1: The user's employment status.
        marital: The user's marital status.
        state: The user's state.

        # Social Determinants of Health Section

        sdhbills: The user's ability to pay bills.
        sdhemple: The user's employment status.
        sdhfood1: The user's food security.
        sdhstre1: The user's stress levels.
        sdhutils: The user's utility payments.
        sdhtrnsp: The user's transportation.

        # Chronic Conditions and Medical History Section

        hvarth4: The user's heart health.
        diabete4: The user's diabetes status.
        cholchk3: The user's cholesterol check.
        bpmeds1: The user's blood pressure medication.
        bphigh6: The user's high blood pressure.
        cvdstrk3: The user's stroke status.
        cvdcrhd4: The user's heart disease status.
        chckdny2: The user's kidney check.
        cholmed3: The user's cholesterol medication.
    """

    # Create the features object list
    ml_features: MLFeaturesMap = create_features()

    # 1. General Health Section
    ######################################################################

    poorhlth = build_form_item(ml_features['POORHLTH'])
    physhlth = build_form_item(ml_features['PHYSHLTH'])
    genhlth = build_form_item(ml_features['GENHLTH'])
    diffwalk = build_form_item(ml_features['DIFFWALK'])
    diffalon = build_form_item(ml_features['DIFFALON'])
    checkup1 = build_form_item(ml_features['CHECKUP1'])

    # Mental Health Section
    ######################################################################

    addepev3 = build_form_item(ml_features['ADDEPEV3'])
    acedeprs = build_form_item(ml_features['ACEDEPRS'])
    sdlonely = build_form_item(ml_features['SDLONELY'])
    lsatisfy = build_form_item(ml_features['LSATISFY'])
    emtsuprt = build_form_item(ml_features['EMTSUPRT'])
    decide = build_form_item(ml_features['DECIDE'])
    cdsocia1 = build_form_item(ml_features['CDSOCIA1'])

    # Lifestyle and Habits Section
    #####################################################################

    smokday2 = build_form_item(ml_features['SMOKDAY2'])
    alcday4 = build_form_item(ml_features['ALCDAY4'])
    marijan1 = build_form_item(ml_features['MARIJAN1'])
    exeroft1 = build_form_item(ml_features['EXEROFT1'])
    usenow3 = build_form_item(ml_features['USENOW3'])

    # Socioeconomic Factors Section
    #####################################################################

    income3 = build_form_item(ml_features['INCOME3'])
    educa = build_form_item(ml_features['EDUCA'])
    employ1 = build_form_item(ml_features['EMPLOY1'])
    marital = build_form_item(ml_features['MARITAL'])
    state = build_form_item(ml_features['STATE'])

    # Social Determinants of Health Section
    #####################################################################

    sdhbills = build_form_item(ml_features['SDHBILLS'])
    sdhemple = build_form_item(ml_features['SDHEMPLY'])
    sdhfood1 = build_form_item(ml_features['SDHFOOD1'])
    sdhstre1 = build_form_item(ml_features['SDHSTRE1'])
    sdhutils = build_form_item(ml_features['SDHUTILS'])
    sdhtrnsp = build_form_item(ml_features['SDHTRNSP'])
    cdshous1 = build_form_item(ml_features['CDHOUS1'])

    # Chronic Conditions and Medical History Section
    #####################################################################

    hvarth4 = build_form_item(ml_features['HAVARTH4'])
    diabete4 = build_form_item(ml_features['DIABETE4'])
    cholchk3 = build_form_item(ml_features['CHOLCHK3'])
    bpmeds1 = build_form_item(ml_features['BPMEDS1'])
    bphigh6 = build_form_item(ml_features['BPHIGH6'])
    cvdstrk3 = build_form_item(ml_features['CVDSTRK3'])
    cvdcrhd4 = build_form_item(ml_features['CVDCRHD4'])
    chckdny2 = build_form_item(ml_features['CHCKDNY2'])
    cholmed3 = build_form_item(ml_features['CHOLMED3'])

    # Submit Button
    submit_button = SubmitField('Submit')


def process_form(form: MlInputForm):
    """
    ML Input Form post processing function.
    Process validation and data from the form.

    Processing includes:
    - Get the selected key and value for each form field
    """

    for field in form:
        if isinstance(field, DescriptiveSelectField):
            field.selected = next(
                ((k, v) for k, v in field.choices if k == field.data),
                None
            )

    return True
