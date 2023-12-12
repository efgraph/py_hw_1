import os
import pandas as pd
import re
from sqlalchemy import create_engine
from config.config import settings


def convert_df():
    filesnames = os.listdir('datasets')
    dfs = {}
    for f in filesnames:
        if 'csv' in f:
            name = re.search(r'_(\w+)', f)
            dfs[name.group(1)] = pd.read_csv(f'datasets/{f}', encoding='utf-8')
    df_result = dfs['clients'][
        ['ID', 'AGE', 'GENDER', 'CHILD_TOTAL', 'DEPENDANTS', 'SOCSTATUS_WORK_FL', 'SOCSTATUS_PENS_FL']]
    df_total_loan = pd.merge(dfs['loan'], dfs['close_loan'], on='ID_LOAN')
    df_loan_num_total = df_total_loan.value_counts('ID_CLIENT').reset_index().rename(
        columns={'count': 'LOAN_NUM_TOTAL'})
    df_result_num_loan = pd.merge(df_loan_num_total, df_result, left_on='ID_CLIENT', right_on='ID')
    df_result_num_loan.drop(columns=['ID_CLIENT'], inplace=True)
    df_close_loan_view = pd.merge(dfs['close_loan'], dfs['loan'], on='ID_LOAN')
    df_pivot_closed_loans = df_close_loan_view.pivot(index='ID_LOAN', columns='CLOSED_FL', values='ID_CLIENT')
    df_pivot_result = df_pivot_closed_loans.reset_index()
    df_pivot = pd.DataFrame()
    df_pivot['ID_CLIENT'] = df_pivot_result.iloc[:, [2]]
    df_pivot['ID_LOAN'] = df_pivot_result['ID_LOAN']
    df_pivot = df_pivot[df_pivot['ID_CLIENT'].notna()]
    df_pivot['ID_CLIENT'] = df_pivot['ID_CLIENT'].astype(int)
    df_piv_result = df_pivot.value_counts('ID_CLIENT').reset_index()
    df_result_count_loan = df_result_num_loan.copy()
    df_result_with_loan = pd.merge(df_result_count_loan, df_piv_result, left_on='ID', right_on='ID_CLIENT', how='left')
    df_result_with_loan = df_result_with_loan.drop(columns=['ID_CLIENT'])
    df_result_with_loan['LOAN_NUM_CLOSED'] = df_result_with_loan['count'].fillna(0).astype(int)
    df_result_with_loan = df_result_with_loan.drop(columns=['count'])
    df_result_with_income = pd.merge(df_result_with_loan, dfs['salary'], left_on='ID', right_on='ID_CLIENT')
    df_result_with_income.drop(columns=['FAMILY_INCOME', 'ID_CLIENT'], inplace=True)
    result_with_target = pd.merge(df_result_with_income, dfs['target'], left_on='ID', right_on='ID_CLIENT')
    result_with_target = result_with_target.drop(columns=['ID_CLIENT'])
    return result_with_target


def load():
    df = convert_df()
    engine = create_engine(settings.db_dsn)
    df.to_sql('bank_data', engine)


if __name__ == '__main__':
    load()
