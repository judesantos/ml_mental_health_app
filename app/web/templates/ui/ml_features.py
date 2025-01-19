"""
This module contains the list of machine learning features for the
CDC Behavioral Risk Factor Surveillance System (BRFSS) mental health data.

The list of features is used to generate the machine learning input form
for the mental health classification model.

Classes:
    Validation: A dictionary class for validation rules
    MLFeature: A class for machine learning data features
    MLFeaturesMap: A dictionary class for MLFeature objects

Functions:
    create_features: Initialize and return an instance of a predefined list of
        ML features for the input form.
"""

from wtforms.validators import DataRequired


class Validation(dict):
    """
    Vallidation class will serve as container for validation rules
    required to accept input when user fills out the mental health
    questionnaire.
    """
    pass


class MLFeature:
    """
    The MLFeature class is a property element describing the
    requirements and rules required to accept input of a dataset feature.

    The class will be used to generate the machine learning input form items.

    Attributes:
        id (str): The unique identifier for the feature.
        options (dict): The options for the feature.
        label (str): The label for the feature.
        question (str): The question for the feature.
        validation (Validation): The validation rules for the feature.
    """

    def __init__(self, id, options, label, question, validators):
        """
        The constructor for the MLFeature class.

        Args:
            id (str): The unique identifier for the feature.
            options (dict): The options for the feature.
            label (str): The label for the feature.
            question (str): The question for the feature.
            validation (Validation): The validation rules for the feature.
        """

        self.id: str = id
        self.options: dict = options
        self.label: str = label
        self.question: str = question
        self.validators: list = validators

    def get_options(self):
        """
        Converts the property 'options' from its dictionary form
        into a list of tuples.

        Returns:
            list: A list of tuples containing the options for the feature.
        """

        # Reverse the dictionary index from key/value, to value/key.
        # Flask WT select input elements always use the
        # right side of tuple as the key.
        rev = {value: key for key, value in self.options.items()}
        # Convert to list of tuples with value/key (e.g. ('77', 'Not Sure'))
        options = list(rev.items())

        return options


class MLFeaturesMap(dict[str, MLFeature]):
    """
    MLFeaturesMap class is a dictionary class for MLFeature objects.
    """
    pass


def create_features() -> MLFeaturesMap:
    """
    Initialize and return an instance of a predefined list of ML features for
    the input form.

    Returns:
        dict: A dictionary of ML features for the mental health
            classification model input form.

    """

    ml_features = MLFeaturesMap()

    # 1. General Health Section
    ########################################################################

    feat = MLFeature(
        id='POORHLTH',
        options={'1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
                 '6': '6', '7': '7', '8': '8', '9': '9', '10': '10',
                 '11': '11', '12': '12', '13': '13', '14': '14',
                 '15': '15', '16': '16', '17': '17', '18': '18',
                 '19': '19', '20': '20', '21': '21', '22': '22',
                 '23': '23', '24': '24', '25': '25', '26': '26',
                 '27': '27', '28': '28', '29': '29', '30': '30', 'None': '88',
                 'Not Sure': '77', 'Refuse to answer': '99'},
        label='Poor Health',
        question='During the past 30 days, for about how many days did '
        'poor physical or mental health keep you from doing your usual '
        'activities, such as self-care, work, or recreation?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='PHYSHLTH',
        options={'1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
                 '6': '6', '7': '7', '8': '8', '9': '9', '10': '10',
                 '11': '11', '12': '12', '13': '13', '14': '14',
                 '15': '15', '16': '16', '17': '17', '18': '18',
                 '19': '19', '20': '20', '21': '21', '22': '22',
                 '23': '23', '24': '24', '25': '25', '26': '26',
                 '27': '27', '28': '28', '29': '29', '30': '30', 'None': '88',
                 'Not Sure': '77', 'Refuse to answer': '99'},
        label='Physical Health',
        question='About your physical health, which includes physical '
        'illness and injury, for how many days during the past 30 days '
        'was your physical health not good?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='GENHLTH',
        options={'Excellent': '1', 'Very Good': '2',
                 'Good': '3', 'Fair': '4', 'Poor': '5', 'Not Sure': '7',
                 'Refused': '9'},
        label='General Health',
        question="Would you say that in general your health is:",
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='DIFFWALK',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Difficulty walking',
        question="Do you have serious difficulty walking or climbing stairs?",
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='DIFFALON',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Difficulty doing errands alone',
        question='Because of a physical, mental, or emotional condition, '
        'do you have difficulty doing errands alone such as visiting a '
        'doctor´s office or shopping?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='CHECKUP1',
        options={'Less than 1 year': '1', 'Less than 2 years': '2',
                 '3': 'Less than 5 years', '5+ Years': '4', 'Not Sure': '7',
                 'Never': '8', 'Refused': '9'},
        label='Length of time since last routine checkup',
        question='About how long has it been since you last visited a '
        'doctor for a routine checkup?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='DIFFDRES',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Difficulty Dressing or Bathing',
        question='Do you have difficulty dressing or bathing?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    # 2. Mental Health Section
    ########################################################################

    feat = MLFeature(
        id='ADDEPEV3',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='(Ever told) you had a depressive disorder',
        question='(Ever told) (you had) a depressive disorder (including '
        'depression, major depression, dysthymia, or minor depression)?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='ACEDEPRS',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Live With Anyone Depressed, Mentally Ill, Or Suicidal?',
        question='Did you live with anyone who was depressed, mentally ill, '
        'or suicidal?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='SDLONELY',
        options={'Always': '1', 'Usually': '2', 'Sometimes': '3',
                 'Rarely': '4', 'Never': '5', 'Not Sure': '7',
                 'Refused': '9'},
        label='How often do you feel lonely?',
        question="How often do you feel lonely?  Is it…",
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='LSATISFY',
        options={'Very Satisfied': '1', 'Satisfied': '2',
                 'Dissatisfied': '3', 'Very Dissatisfied': '4',
                 'Not Sure': '7', 'Refused': '9'},
        label='Satisfaction with life',
        question="In general, how satisfied are you with your life?",
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='EMTSUPRT',
        options={'Always': '1', 'Usually': '2', 'Sometimes': '3',
                 'Rarely': '4', 'Never': '5', 'Not Sure': '7',
                 'Refused': '9'},
        label='How often get emotional support needed',
        question='How often do you get the social and emotional support '
        'you need?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='DECIDE',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Difficulty Concentrating or Remembering',
        question='Because of a physical, mental, or emotional condition, '
        'do you have serious difficulty concentrating, remembering, '
        'or making decisions?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='CDSOCIA1',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='''Does difficulties with thinking or memory interfere with
            work or social activities''',
        question='During the past 12 months, have your difficulties '
        'with thinking or memory interfered with your ability to work '
        'or volunteer?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='CDDISCU1',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='''Have you discussed your difficulties with thinking
        with a health care provider?''',
        question='''Have you or anyone else discussed your difficulties
        with thinking or memory with a health care provider?''',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='CIMEMLO1',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='''Have you experienced difficulties with thinking or memory
        that is happening more often or is getting worse?''',
        question='''During the past 12 months, have you experienced
        difficulties with thinking or memory that are happening more
        often or are getting worse?''',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    # 3. Lifestyle and Habits Section
    ########################################################################

    feat = MLFeature(
        id='SMOKDAY2',
        options={'Every Day': '1', 'Some Days': '2',
                 'Not at All': '3', 'Not Sure': '7', 'Refused': '9'},
        label='Frequency of Days Now Smoking',
        question='Do you now smoke cigarettes every day, some days, or not '
        'at all?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='ALCDAY4',
        options={'1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
                 '6': '6', '7': '7', '8': '8', '9': '9', '10': '10',
                 '11': '11', '12': '12', '13': '13', '14': '14',
                 '15': '15', '16': '16', '17': '17', '18': '18', '19': '19',
                 '20': '20', '21': '21', '22': '22', '23': '23',
                 '24': '24', '25': '25', '26': '26', '27': '27', '28':
                 '28', '29': '29', '30': '30', 'None': '888',
                 'Not Sure': '777', 'Refuse to answer': '999'},
        label='Days in past 30 had alcoholic beverage',
        question='During the past 30 days, how many days '
        'per month did you have at least one drink of any alcoholic  '
        'beverage?  (A 40 ounce beer would count as 3 drinks, '
        'or a cocktail drink with 2 shots would count as 2 drinks.)',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='MARIJAN1',
        options={'1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
                 '6': '6', '7': '7', '8': '8', '9': '9', '10': '10',
                 '11': '11', '12': '12', '13': '13', '14': '14',
                 '15': '15', '16': '16', '17': '17', '18': '18',
                 '19': '19', '20': '20', '21': '21', '22': '22',
                 '23': '23', '24': '24', '25': '25', '26': '26',
                 '27': '27', '28': '28', '29': '29', '30': '30', 'None': '88',
                 'Not Sure': '77', 'Refuse to answer': '99'},
        label='''During the past 30 days, on how many days did you use
            marijuana or hashish?''',
        question='During the past 30 days, on how many days did you use '
        'marijuana or cannabis?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='EXEROFT1',
        options={'1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
                 '6': '6', '7': '7', '8': '8', '9': '9', '10': '10',
                 '11': '11', '12': '12', '13': '13', '14': '14',
                 '15': '15', '16': '16', '17': '17', '18': '18',
                 '19': '19', '20': '20', '21': '21', '22': '22',
                 '23': '23', '24': '24', '25': '25', '26': '26',
                 '27': '27', '28': '28', '29': '29', '30': '30',
                 'Not Sure': '777', 'Refuse to answer': '999'},
        label='How Many Times Walking, Running, Jogging, or Swimming',
        question='How many times per month did you take '
        'part in this activity during the past month?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='USENOW3',
        options={'Every Day': '1', 'Some Days': '2',
                 'Not at All': '3', 'Not Sure': '7', 'Refused': '9'},
        label='Use of Smokeless Tobacco Products',
        question='Do you currently use chewing '
        'tobacco, snuff, or snus every day, some days, or not at all? '
        '(Snus (Swedish for snuff) is a moist smokeless tobacco, '
        'usually sold in small pouches that are placed under the '
        'lip against the gum.)',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='FIREARM5',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Any Firearms in Hom',
        question='Are any firearms now kept in or around your home?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    # 4. Socioeconomic Factors Section
    #######################################################################

    feat = MLFeature(
        id='INCOME3',
        options={'<$10,000': '1', '$10,000 to <$15,000': '2',
                 '$15,000 to <$20,000': '3', '$20,000 to <$25,000': '4',
                 '$25,000 to <$35,000': '5', '$35,000 to <$50,000': '6',
                 '$50,000 to <$75,000': '7', '$75,000 to <$100,000': '8',
                 '$100,000 to <$150,000': '9', '$150,000 to <$200,000': '10',
                 '$200,000 or more': '11', 'Not Sure': '77', 'Refused': '99'},
        label='Income Level',
        question='Is your annual household income from all sources:',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='EDUCA',
        options={'Never attended school or only kindergarten': '1',
                 'Grades 1 through 8 (Elementary)': '2',
                 'Grades 9 through 11 (Some high school)': '3',
                 'Grade 12 or GED (High school graduate)': '4',
                 'College 1 year to 3 years': '5',
                 'College 4 years or more (Graduated)': '6',
                 'Refused': '9'},
        label='Education Level',
        question='What is the highest grade or year of school you '
        'completed?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='EMPLOY1',
        options={'Employed for wages': '1', 'Self-employed': '2',
                 'Out of work for 1 year or more': '3',
                 'Out of work for less than 1 year': '4',
                 'A homemaker': '5', 'A student': '6',
                 'Retired': '7', 'Unable to work': '8', 'Refused': '9'},
        label='Employment Status',
        question="Are you currently…?",
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='SEX',
        options={'Male': '1', 'Female': '2', 'Note Sure': '7',
                 'Refused': '9'},
        label='Are you male or female?',
        question='What was your sex at birth? Was it male or female?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='MARITAL',
        options={'Married': '1', 'Divorced': '2', 'Widowed': '3',
                 'Separated': '4', 'Never married':
                 '5', 'Living with a partner': '6', 'Refused': '9'},
        label='Marital Status',
        question="Are you: (marital status)",
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='ADULT',
        options={'Yes': '1', 'No': '2'},
        label='Adult?',
        question="Are you 18 years of age or older?",
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='RRCLASS3',
        options={'White': '1', 'Black': '2', 'Hispanic or Latino': '3',
                 'Asian': '4', 'Native Hawaiian or Pacific Islander': '5',
                 'American Indian or Alaska Native': '6', 'Mixed Race': '7',
                 'Other': '8', 'Not Sure': '77', 'Refused': '99'},

        label='How do other people usually classify you in this country?',
        question='''How do other people usually classify you in
        this country? Would you say White, Black or African American,
        Hispanic or Latino, Asian, Native Hawaiian or Other Pacific Islander,
        American Indian or Alaska Native, or some other group?''',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='QSTLANG',
        options={'English': '1', 'Spanish': '2'},
        label='Language identifier',
        question='Language spoken',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='STATE',
        options={'Alabama': '1', 'Alaska': '2', 'Arizona': '4',
                 'Arkansas': '5', 'California': '6', 'Colorado': '8',
                 'Connecticut': '9', 'Delaware': '10',
                 'District of Columbia': '11', 'Florida': '12',
                 'Georgia': '13', 'Hawaii': '15',
                 'Idaho': '16', 'Illinois': '17', 'Indiana': '18',
                 'Iowa': '19', 'Kansas': '20', 'Kentucky': '21',
                 'Louisiana': '22', 'Maine': '23', 'Maryland': '24',
                 'Massachusetts': '25', 'Michigan': '26', 'Minnesota': '27',
                 'Mississippi': '28', 'Missouri': '29', 'Montana': '30',
                 'Nebraska': '31', 'Nevada': '32', 'New Hampshire': '33',
                 'New Jersey': '34', 'New Mexico': '35', 'New York': '36',
                 'North Carolina': '37', 'North Dakota': '38', 'Ohio': '39',
                 'Oklahoma': '40', 'Oregon': '41', 'Pennsylvania': '42',
                 'Rhode Island': '44', 'South Carolina': '45',
                 'South Dakota': '46', 'Tennessee': '47', 'Texas': '48',
                 'Utah': '49', 'Vermont': '50', 'Virginia': '51',
                 'Washington': '53', 'West Virginia': '54', 'Wisconsin': '55',
                 'Wyoming': '56', 'Guam': '66', 'Puerto Rico': '72',
                 'Virgin Islands': '78'},
        label='State',
        question="Which state do you reside in.",
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='VETERAN3',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Are You A Veteran',
        question='''Have you ever served on active duty in the
        United States Armed Forces, either in the regular military
        or in a National Guard or military reserve unit?''',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    # 5 Social Determinants of Health Section
    ########################################################################

    feat = MLFeature(
        id='MEDCOST1',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Could Not Afford To See Doctor',
        question='''Was there a time in the past 12 months when you needed
        to see a doctor but could not because you could not afford it?''',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='SDHBILLS',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Were you not able to pay your bills?',
        question='During the last 12 months, was there a time when you '
        'were not able to pay your mortgage, rent or utility bills?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='SDHEMPLY',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Have you lost employment or had hours reduced?',
        question='In the past 12 months have you lost employment or '
        'had hours reduced?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='SDHFOOD1',
        options={'Always': '1', 'Usually': '2', 'Sometimes': '3',
                 'Rarely': '4', 'Never': '5', 'Not Sure': '7',
                 'Refused': '9'},
        label='''How often did the food that you bought not last, and you
            didn’t have money to get more?''',
        question='During the past 12 months how often did the food '
        'that you bought not last, and you didn’t have money to get '
        'more? Was that…',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='SDHSTRE1',
        options={'Always': '1', 'Usually': '2', 'Sometimes': '3',
                 'Rarely': '4', 'Never': '5', 'Not Sure': '7',
                 'Refused': '9'},
        label='How often have you felt this kind of stress?',
        question='Within the last 30 days, how often have you felt '
        'this kind of stress?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='SDHUTILS',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='''Were you not able to pay utility bills or threatened to
        lose service?''',
        question='During the last 12 months was there a time when an '
        'electric, gas, oil, or water company threatened to shut off '
        'services?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='SDHTRNSP',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='''Has a lack of reliable transportation kept you from
            appointments, meetings, work, or getting things needed''',
        question='During the past 12 months has a lack of reliable '
        'transportation kept you from medical appointments, meetings, '
        'work, or from getting things needed for daily living?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='CDHOUS1',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='''Given up day-to-day chores due to difficulties with thinking
            or memory''',
        question='During the past 12 months, have your difficulties with '
        'thinking or memory interfered with day-to-day activities, '
        'such as managing medications, paying bills, or keeping track '
        'of appointments?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='FOODSTMP',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='''During the past 12 months have you received food stamps''',
        question='''During the past 12 months, have you received food stamps,
        also called SNAP, the Supplemental Nutrition Assistance
        Program on an EBT card?''',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    # 5. Chronic Conditions and Medical History Section
    #######################################################################

    feat = MLFeature(
        id='PREGNANT',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Pregnancy Status',
        question='To your knowledge, are you now pregnant?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='ASTHNOW',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Still Have Asthma',
        question='Do you still have asthma?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='HAVARTH4',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Told Had Arthritis',
        question='(Ever told) (you had) some form of arthritis, '
        'gout, lupus, or fibromyalgia?  (Arthritis diagnoses include: '
        'rheumatism, polymyalgia rheumatica; osteoarthritis '
        '(not osteporosis); tendonitis, bursitis, bunion, tennis '
        'elbow; carpal tunnel syndrome, tarsal tunnel syndrome; joint '
        'infection, etc.)',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='CHCSCNC1',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Skin cancer, not melanoma',
        question='(Ever told) (you had) skin cancer that is not melanoma?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='CHCOCNC1',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Melanoma or other types of cancer',
        question='''(Ever told) (you had) melanoma or any other
        types of cancer?''',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='DIABETE4',
        options={'Yes': '1', 'During Pregnancy': '2', 'No': '3',
                 'Pre-diabetes': '4',   'Not Sure': '7', 'Refused': '9'},
        label='(Ever told) you had diabetes',
        question='(Ever told) (you had) diabetes?  (If ´Yes´ and '
        'respondent is female, ask ´Was this only when you were '
        'pregnant?. If Respondent says pre-diabetes '
        'or borderline diabetes, use response code 4.)',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='CHCCOPD3',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='C.O.P.D. emphysema or chronic bronchitis',
        question='''(Ever told) (you had) C.O.P.D.
        (chronic obstructive pulmonary disease),
        emphysema or chronic bronchitis?''',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='CHOLCHK3',
        options={'Never': '1', 'Within the past year': '2',
                 'Within the past 2 years': '3',
                 'Within the past 3 years': '4',
                 'Within the past 4 years': '5',
                 'Within the past 5 years': '6',
                 'Not Sure': '7', 'Refused': '9'},
        label='How Long since Cholesterol Checked',
        question='About how long has it been since you last had '
        'your cholesterol checked?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='BPMEDS1',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Currently Taking Prescription Blood Pressure Medication',
        question='Are you currently taking prescription medicine '
        'for your high blood pressure?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='BPHIGH6',
        options={'Yes': '1', 'During Pregnancy': '2', 'No': '3',
                 'Pre-hypertensive': '4',   'Not Sure': '7', 'Refused': '9'},
        label='Ever Told Blood Pressure High',
        question='Have you ever been told by a doctor, nurse or other '
        'health professional that you have high blood pressure? '
        '(If ´Yes´ and respondent is female, ask ´Was this only when '
        'you were pregnant?´.)',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='CVDSTRK3',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Ever Diagnosed with a Stroke',
        question="(Ever told) (you had) a stroke.",
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='CVDCRHD4',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Ever Diagnosed with Angina or Coronary Heart Disease',
        question="(Ever told) (you had) angina or coronary heart disease?",
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='CHCKDNY2',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Ever told you have kidney disease?',
        question='''Not including kidney stones, bladder infection or
            incontinence, were you ever told you had kidney disease?''',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    feat = MLFeature(
        id='CHOLMED3',
        options={'Yes': '1', 'No': '2', 'Not Sure': '7', 'Refused': '9'},
        label='Currently taking medicine for high cholesterol',
        question='Are you currently taking medicine prescribed by your '
        'doctor or other health professional for your cholesterol?',
        validators=[DataRequired()]
    )
    ml_features[feat.id] = feat

    return ml_features
