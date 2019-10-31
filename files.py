import boto3

s3 = boto3.resource('s3')

class FileProxy:
    def load_from_file(self, name):
        pass

    def store_to_file(self, name):
        pass


# When using S3, load from the bucket
class S3FileProxy(FileProxy):
    def __init__(self, bucket, file):
        self._bucket = bucket
        self._file = file

    def load_from_file(self):
        bucket = s3.Bucket(self._bucket)
        object = bucket.Object(self._file)
        response = object.get()
        file_stream = response['Body']
        return file_stream.read().decode('utf-8')

    def store_to_file(self, content):
        bucket = s3.Bucket(self._bucket)
        object = bucket.Object(self._file)
        object.put(Body=content)


# For local machine, work with files
class LocalFileProxy(FileProxy):
    def __init__(self, file):
        self._file = file

    def load_from_file(self):
        return open(self._file).read()

    def store_to_file(self, content):
        with open(self._file, 'w') as f:
            f.write(content)
