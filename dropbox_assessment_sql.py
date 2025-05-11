import pandas as pd
import sqlite3

df = pd.read_csv('ca_takehome_assessment.csv')

conn = sqlite3.connect('your_database.db')  # or ':memory:' for a temporary DB

df.to_sql('your_table', conn, if_exists='replace', index=False)

result = pd.read_sql_query("SELECT * FROM your_table LIMIT 5;", conn)
print(result)

query = """
select support_channel,
    round(
        100.0 * sum(case when survey_score in (4,5) then 1 else 0 end)/count(survey_score),2)
    as csat_percent
from your_table
where survey_score is not null
group by support_channel
order by csat_percent desc
"""
result = pd.read_sql_query(query, conn)
print(result)

query2 = """
select user_type, count(*) as ticket_count, round(100 * count(*) / (select count(*) from tickets), 2) as proportion
from your_table
group by user_type
order by proportion
"""

result2 = pd.read_sql_query(query2, conn)
print(result)