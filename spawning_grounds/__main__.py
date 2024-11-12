import logging
import os
import random
import uuid

import boto3

from spawning_grounds.config import load_config

log = logging.getLogger(__file__)

KILOBYTE = 1024


def main():
    config = load_config()

    session = boto3.session.Session(
        aws_access_key_id=config.access_key_id,
        aws_secret_access_key=config.secret_access_key,
        region_name=config.region,
    )
    s3 = session.resource("s3")
    bucket = s3.Bucket(config.bucket)

    for dataset_name, values in config.datasets.items():
        files = [file for file in bucket.objects.filter(Prefix=dataset_name)]
        current_count = len(files)
        count_to_add = values["count"] - current_count
        count_to_add = count_to_add if count_to_add > 0 else 0

        if count_to_add > 0:
            log.info(f'adding {count_to_add} files to dataset "{dataset_name}"')
        else:
            log.info(
                f'dataset "{dataset_name}" has {current_count} files already, skipping'
            )

        size = KILOBYTE * values["size_kb"]
        for i in range(count_to_add):
            log.info(f'uploading {i + 1} / {count_to_add} to "{dataset_name}"...')
            file_id = uuid.uuid4()
            key = f'{dataset_name}/{file_id}.{random.choice(values["extensions"])}'
            body = os.urandom(size)
            bucket.put_object(Key=key, Body=body)

        log.info(f'dataset "{dataset_name}" is done')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
