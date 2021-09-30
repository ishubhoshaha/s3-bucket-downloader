import os
import argparse
from collections import namedtuple
from alive_progress import alive_it
import boto3

user_input_format = namedtuple('user_input', ['src', 'dest'])

class S3Helper:
    def __init__(self):
        self.s3 = boto3.client('s3')

    def get_all_objects(self, bucket_name, prefix=""):
        next_token = ""
        keys = []
        dirs = []
        base_kwargs = {
            'Bucket': bucket_name,
            'Prefix': prefix
        }
        while next_token is not None:
            kwargs = base_kwargs.copy()
            if next_token != '':
                kwargs.update({'ContinuationToken': next_token})
            list_s3_objects = self.s3.list_objects_v2(**kwargs)
            contents = list_s3_objects.get('Contents')

            # print(contents)
            for content in contents:
                key = content.get('Key')
                if key[-1] != '/':
                    keys.append(key)
                else:
                    dirs.append(key)
            next_token = list_s3_objects.get('NextContinuationToken')

        return keys,dirs

    def download_object_locally(self, bucket_name, keys, dirs, destination=None):
        if not os.path.exists(destination):
            os.makedirs(os.path.dirname(destination))
        # print(bucket_name, destination, dirs, keys)
        for dir in dirs:
            dest_pathname = os.path.join(destination, dir)
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))

        for key in alive_it(keys):
            # for key in keys:
            dest_pathname = os.path.join(destination, key)
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
            self.s3.download_file(bucket_name, key, dest_pathname)



def parse_user_input():
    parser = argparse.ArgumentParser(description="S3 Bucket Downloader")
    parser.add_argument('-b', '--bucket', type=str, help='S3 bucket name', required=True)
    parser.add_argument('-d', '--destination', type=str, help='Download to', required=True)
    args = parser.parse_args()
    src = args.bucket
    dest = args.destination
    return src, dest

def main(user_input):
    prefix = ""
    s3_interface = S3Helper()
    keys, dirs = s3_interface.get_all_objects(user_input.src, prefix)
    s3_interface.download_object_locally(user_input.src, keys, dirs, user_input.dest)

if __name__ == '__main__':
    user_input = user_input_format._make(parse_user_input())
    main(user_input)