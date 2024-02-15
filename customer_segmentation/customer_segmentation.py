import kaggle
import os
import pandas as pd


def download_dataset(download: bool = False) -> str:
    """Download the data setfrom Kaggle
    Args:
        download (bool, optional): Flag to download the dataset. Defaults to False.
    Returns:
        None
    """
    fname = 'PRODUCT SALES.csv'
    if os.path.exists(fname) or not download:
        print('Skipping downl;oad as the file already exists')
    else:
        print('Starting download of the customer segmentation data from Kaggle')
        kaggle.api.dataset_download_files(
            dataset='kanyianalyst/customer-age-group-segmentation',
            path='.',
            force=True,
            quiet=False,
            unzip=True
            )
    return fname


def load_file(fname: str) -> pd.DataFrame:
    """Load the csv file into local memory, rename the headers, and
    optjimise the data types.
    
    Args:
        fname (str): The name of the customer segmentation file
        
    Returns:
        pd.DataFrame: The customer segmentation data
    """
    header = [
        'date', 'day', 'month', 'year', 'customer_age', 'age_group',
        'age_group_id', 'customer_gender', 'country', 'product_category',
        'order_quantity', 'unit_cost', 'unit_price', 'profit', 'cost',
        'revenue'
    ]
    dtype_map = dict(Customer_Age=int,
                     Age_Group_NUMBER=int,
                     Order_Quantity=int,
                     Unit_Cost=float,
                     Unit_Price=float,
                     Profit=float,
                     Cost=float,
                     Revenue=float)
    df = pd.read_csv(fname,
                     sep=',',
                     header=0,
                     names=header,
                     dtype=dtype_map,
                     parse_dates=['date'])
    df[['age_group', 'customer_gender', 'country', 'product_category']] = df[[
        'age_group', 'customer_gender', 'country', 'product_category'
    ]].astype('category')
    # Recreating date columns since the original dataset is incorrect
    df.drop(columns=['day', 'month', 'year'], inplace=True)
    df['month'] = pd.to_datetime(df['date']).dt.month
    df['day'] = pd.to_datetime(df['date']).dt.day
    df['year'] = pd.to_datetime(df['date']).dt.year
    return df

def customer_age_analysis(df: pd.DataFrame):
    df_filtered = df[['month', 'customer_age', 'order_quantity', 'unit_cost', 'unit_price', 'profit', 'cost', 'revenue']]
    df_filtered.corr()
    return


def main():
    fname = download_dataset()
    df = load_file(fname)
    customer_age_analysis(df)


if __name__ == "__main__":
    main()
