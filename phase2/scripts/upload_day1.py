import sys,os
from s3_ingest.client import S3Client

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



bucket = "capstone-project-bucket-12345"
date_partition = "dt=2026-07-11"

files = {
    f"raw/customers/{date_partition}/customers.csv": "data/customers.csv",
    f"raw/products/{date_partition}/products.csv": "data/products.csv",
    f"raw/orders/{date_partition}/orders_day1.json": "data/orders_day1.json",
    f"raw/order_items/{date_partition}/order_items_day1.json": "data/order_items_day1.json"
}

def main():
    client = S3Client(profile=os.getenv("AWS_PROFILE","default"),
                      region=os.getenv("AWS_REGION","us-east-1"))
    for key, path in files.items():
        client.upload_file(bucket, key, path)
    
    # Try uploading a file that doesn't exist locally
    client.upload_file("capstone-project-bucket-12345",
                       "raw/test/missing.csv",
                       "data/missing.csv")

if __name__ == "__main__":
    main()
