import csv
import pandas as pd


def write_to_file(filename, email, mobile_friendly, ssl_active):
    with open(filename, 'a+') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow([email,ssl_active, mobile_friendly])


def get_all_from_email(filename):
    col = ['email', 'mobile_friendly', 'ssl_active']
    df = pd.read_csv(filename)
    df.columns = col
    return df['email'].unique().tolist()

