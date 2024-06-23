from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd


def encode(dataframe):
    columns = {'Your Current Country.': 'country',
               'Your Current Zip Code / Pin Code': 'zip_code',
               'Your Gender': 'gender',
               'Which of the below factors influence the most about your career aspirations ?': 'influential_factors',
               'Would you definitely pursue a Higher Education / Post Graduation outside of India ? If only you have to self sponsor it.': 'higher_education',
               'How likely is that you will work for one employer for 3 years or more ?': 'experience',
               'Would you work for a company whose mission is not clearly defined and publicly posted.': 'unclear_mission',
               'How likely would you work for a company whose mission is misaligned with their public actions or even their product ?': 'misalign_actions',
               'How likely would you work for a company whose mission is not bringing social impact ?': 'social_impact',
               'What is the most preferred working environment for you.': 'working_environment',
               'Which of the below Employers would you work with.': 'employers',
               'Which type of learning environment that you are most likely to work in ?': 'learning_environment',
               'Which of the below careers looks close to your Aspirational job ?': 'aspirational_job',
               'What type of Manager would you work without looking into your watch ?': 'manager_preferences',
               'Which of the following setup you would like to work ?': 'team_setup', }

    dataframe.rename(columns=columns, inplace=True)

    dataframe.head()

    """# Encode"""

    df_encoded = dataframe.copy()

    # Encode for country
    encode_co = {"India": 0,
                 "United Arab Emirates": 1,
                 "United States of America": 2,
                 "Germany": 3, }
    df_encoded['country'] = df_encoded['country'].apply(lambda x: encode_co[x])

    # Zero for Female and One for Male
    df_encoded['gender'] = df_encoded['gender'].apply(lambda x: 0 if x.lower() == 'female' else 1)

    # Encode for influential factors
    encode_if = {"People who have changed the world for better": 0,
                 "Social Media like LinkedIn": 1,
                 "People from my circle, but not family members": 2,
                 "Influencers who had successful careers": 3,
                 "My Parents": 4, }
    df_encoded['influential_factors'] = df_encoded['influential_factors'].apply(lambda x: encode_if[x])

    # -1 for an absolutely No, 0 for No but, 1 for Yes
    df_encoded['higher_education'] = df_encoded['higher_education'].apply(
        lambda x: 1 if 'yes' in x.lower() else 0 if 'no,' in x.lower() else -1)

    # -1 for No way, 0 for will, 1 for yes
    df_encoded['experience'] = df_encoded['experience'].apply(
        lambda x: 1 if 'will work' in x.lower() else 0 if 'this will' in x.lower() else -1)

    # 0 for No, 1 for Yes
    df_encoded['unclear_mission'] = df_encoded['unclear_mission'].apply(lambda x: 1 if x.lower() == 'yes' else 0)

    # 0 for Not work and 1 for Yes
    df_encoded['misalign_actions'] = df_encoded['misalign_actions'].apply(lambda x: 0 if 'not' in x.lower() else 1)

    # Encode for working environment
    encode_we = {"Fully Remote with No option to visit offices": 0,
                 "Fully Remote with Options to travel as and when needed": 1,
                 "Hybrid Working Environment with less than 15 days a month at office": 2,
                 "Every Day Office Environment": 3,
                 "Hybrid Working Environment with less than 10 days a month at office": 4,
                 "Hybrid Working Environment with less than 3 days a month at office": 5, }
    df_encoded['working_environment'] = df_encoded['working_environment'].apply(lambda x: encode_we[x])

    # Encode for employers
    encode_em = {"Employer who rewards learning and enables that environment": 0,
                 "Employer who pushes your limits by enabling an learning environment, and rewards you at the end": 1,
                 "Employer who appreciates learning and enables that environment": 2,
                 "Employer who pushes your limits and doesn't enables learning environment and never rewards you": 3,
                 "Employers who appreciates learning but doesn't enables an learning environment": 4, }
    df_encoded['employers'] = df_encoded['employers'].apply(lambda x: encode_em[x])

    # Encode for manager preferences
    encode_mp = {"Manager who explains what is expected, sets a goal and helps achieve it": 0,
                 "Manager who sets goal and helps me achieve it": 1,
                 "Manager who clearly describes what she/he needs": 2,
                 "Manager who sets targets and expects me to achieve it": 3,
                 "Manager who sets unrealistic targets": 4, }
    df_encoded['manager_preferences'] = df_encoded['manager_preferences'].apply(lambda x: encode_mp[x])

    df_encoded.head()

    """## Encode 'learning_environment', 'aspirational_job', 'team_setup'"""

    # Split values to list
    df_encoded['learning_environment_list'] = df_encoded['learning_environment'].apply(
        lambda x: [i.strip() for i in x.split(',')])
    df_encoded['aspirational_job_list'] = df_encoded['aspirational_job'].apply(
        lambda x: [i.strip() for i in x.split(',')])
    df_encoded['team_setup_list'] = df_encoded['team_setup'].apply(lambda x: [i.strip() for i in x.split(',')])

    # Apply MultiLabel Binarizer for 'learning_environment'
    mlb_env = MultiLabelBinarizer()
    learning_env_encoded = mlb_env.fit_transform(df_encoded['learning_environment_list'])
    learning_env_df = pd.DataFrame(learning_env_encoded, columns=mlb_env.classes_)

    # Apply MultiLabel Binarizer for 'aspirational_job'
    mlb_job = MultiLabelBinarizer()
    aspirational_job_encoded = mlb_job.fit_transform(df_encoded['aspirational_job_list'])
    aspirational_job_df = pd.DataFrame(aspirational_job_encoded, columns=mlb_job.classes_)

    # Apply MultiLabel Binarizer for 'team_setup'
    mlb_team = MultiLabelBinarizer()
    team_setup_encoded = mlb_team.fit_transform(df_encoded['team_setup_list'])
    team_setup_df = pd.DataFrame(team_setup_encoded, columns=mlb_team.classes_)

    # Change columns name following code convention
    new_env_column_names = [
        'env_' + ''.join([word[0].upper() + word[1:] for word in name.split()]).replace('Or', 'Or').replace('And',
                                                                                                            'And') for
        name in mlb_env.classes_]
    new_job_column_names = ['job_' + ''.join([word[0].upper() + word[1:] for word in name.split()]) for name in
                            mlb_job.classes_]
    new_team_column_names = [
        'team_' + ''.join([word[0].upper() + word[1:] for word in name.split()]).replace('To', 'To') for name in
        mlb_team.classes_]

    # Rename columns
    learning_env_df.columns = new_env_column_names
    aspirational_job_df.columns = new_job_column_names
    team_setup_df.columns = new_team_column_names

    # Add new columns and drop previous
    data = pd.concat([df_encoded, aspirational_job_df, team_setup_df], axis=1)
    data.drop(columns=['learning_environment', 'aspirational_job', 'team_setup', 'learning_environment_list',
                       'aspirational_job_list', 'team_setup_list'], inplace=True)

    return data


def json_df(data):
    columns = ['Your Current Country.',
               'Your Current Zip Code / Pin Code',
               'Your Gender',
               'Which of the below factors influence the most about your career aspirations ?',
               'Would you definitely pursue a Higher Education / Post Graduation outside of India ? If only you have to self sponsor it.',
               'How likely is that you will work for one employer for 3 years or more ?',
               'Would you work for a company whose mission is not clearly defined and publicly posted.',
               'How likely would you work for a company whose mission is misaligned with their public actions or even their product ?',
               'How likely would you work for a company whose mission is not bringing social impact ?',
               'What is the most preferred working environment for you.',
               'Which of the below Employers would you work with.',
               'Which type of learning environment that you are most likely to work in ?',
               'Which of the below careers looks close to your Aspirational job ?',
               'What type of Manager would you work without looking into your watch ?',
               'Which of the following setup you would like to work ?']
    df = pd.DataFrame(columns=columns)
    df.loc[0] = data['datos'].split(';')
    sel_columns = []
    with open("columns.txt", "r") as f:
        sel_columns.extend(f.readlines()[0].strip().split(","))

    data = encode(df)
    for col in sel_columns:
        if col not in data.columns:
            data[col] = 0
    data = data[sel_columns]
    data.drop(columns=["misalign_actions"], inplace=True)

    return data


def decode_pred(prediction):
    if int(prediction) == 0:
        return "Will NOT work for them"
    else:
        return "Will work for them"
