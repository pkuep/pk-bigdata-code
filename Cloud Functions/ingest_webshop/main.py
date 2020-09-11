from google.cloud import storage
from datetime import datetime
import pymysql
 
def ingest_webshop(request):
    """ connects to the webshop database, retrieves all rows from the
        table "sales" and uploads these into a file on GCS
    """
    # connect to the database - replace <cloud SQL IP> with the IP of your cloud SQL server
    conn = pymysql.connect(unix_socket='/cloudsql/<YOUR CONNECTION NAME>', user='root', password='', db='webshop')
 
    # create a string that holds all rows of the table "sales" in a csv-ready format
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM sales')
        rows = cur.fetchall()
        sales = "date, weekday, region, age_group, product, product_group, sales_value\n"
        for row in rows:
            sales += (f'{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}\n')
 
    # create a filename with a timestamp and store the data in a csv file in the datalake
    filename = f"webshop_sales_fromfunction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("pk-gcs")
    blob = bucket.blob(filename)
 
    blob.upload_from_string(sales, content_type='text/csv')