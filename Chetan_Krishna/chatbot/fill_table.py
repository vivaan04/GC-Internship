import pandas as pd
import pymysql
from sqlalchemy import create_engine

# db="esgroadmap"
# uname="admin"
# pwd="hassanarshad1122"
# hostname="esgroadmap.cwco2pchjykw.us-east-2.rds.amazonaws.com"

print("Getting the connection...")
cnx = create_engine(f"mysql+pymysql://root:@localhost/esgroadmap")
conn = cnx.connect()
print("Inserting the columns...")
df = pd.read_csv("../company-universe.csv")
df.to_sql(name='company_universe', con=cnx, if_exists='append', index=False)
print("Executing Query")
query = "SELECT * FROM `company_universe` LIMIT 10;"
df_R = pd.read_sql_query(query, cnx)
df_R.to_csv("test.csv")
print(df_R)

conn.close()