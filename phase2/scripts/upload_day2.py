import boto3
import os

bucket = "capstone-project-bucket-12345"
date_partition = "dt=2026-07-12"

# Notice the "../data/" prefix since script is in scripts/ folder
files = {
    f"raw/orders/{date_partition}/orders_day2.json": "../data/orders_day2.json",
    f"raw/order_items/{date_partition}/order_items_day2.json": "../data/order_items_day2.json"
}

def main():
    session = boto3.Session(profile_name=os.getenv("AWS_PROFILE","default"),
                            region_name=os.getenv("AWS_REGION","us-east-1"))
    s3 = session.client("s3")

    for key, path in files.items():
        try:
            s3.upload_file(path, bucket, key)
            print(f"Uploaded {path} → {key}")
        except Exception as e:
            print(f"Failed to upload {path}: {e}")

    # Test file (will fail if not present)
    try:
        s3.upload_file("../data/missing_day2.csv", bucket, "raw/test/missing_day2.csv")
    except Exception as e:
        print(f"Upload failed: {e}")

if __name__ == "__main__":
    main()
