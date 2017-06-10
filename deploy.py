import os
import sys
import os.path
import yaml

import boto
import boto.s3
import boto.s3.connection

# https://github.com/boto/boto/issues/2836#issuecomment-68682573
# import ssl
#
# _old_match_hostname = ssl.match_hostname
#
# def _new_match_hostname(cert, hostname):
#    if hostname.endswith('.s3.amazonaws.com'):
#       pos = hostname.find('.s3.amazonaws.com')
#       hostname = hostname[:pos].replace('.', '') + hostname[pos:]
#    return _old_match_hostname(cert, hostname)
#
# ssl.match_hostname = _new_match_hostname
# -- https://github.com/boto/boto/issues/2836#issuecomment-68682573

SETTINGS_FILE = os.environ['settings']
settings = yaml.load(open(SETTINGS_FILE).read())

AWS_ACCESS_KEY_ID = settings['AWS_ACCESS_KEY_ID']
AWS_ACCESS_KEY_SECRET = settings['AWS_ACCESS_KEY_SECRET']
BUCKET_LOCATION = getattr(boto.s3.connection.Location, settings['BUCKET_LOCATION'])

bucket_name = settings['BUCKET_NAME']

# source directory
sourceDir = os.path.join(os.getcwd(), 'built/')
# destination directory name (on s3)
destDir = ''
# max size in bytes before uploading in parts. between 1 and 5 GB recommended
MAX_SIZE = 20 * 1000 * 1000
# size of parts when uploading in parts
PART_SIZE = 6 * 1000 * 1000


def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()


def deploy(bucket, uploadFileNames):
    for filename in uploadFileNames:
        sourcepath = os.path.join(sourceDir, filename)
        destpath = os.path.join(destDir, filename)
        print('Uploading %s to Amazon S3 bucket %s' % (sourcepath, bucket_name))
        print("To: %s" % destpath)
        filesize = os.path.getsize(sourcepath)

        if filesize > MAX_SIZE:
            print("multipart upload")
            mp = bucket.initiate_multipart_upload(destpath)
            fp = open(sourcepath, 'rb')
            fp_num = 0
            while fp.tell() < filesize:
                fp_num += 1
                print("uploading part %i" %fp_num)
                mp.upload_part_from_file(fp, fp_num, cb=percent_cb, num_cb=10,
                    size=PART_SIZE)

            mp.complete_upload()
        else:
            print("singlepart upload")
            k = boto.s3.key.Key(bucket)
            k.key = destpath
            k.set_contents_from_filename(sourcepath, cb=percent_cb, num_cb=10)
            print('')


def files_to_upload(path):
    result = []
    for (sDir, dirname, filename) in os.walk(path):
        for fn in filename:
            result.append(os.path.join(sDir.replace(path, ''), fn))

    return result


if __name__ == '__main__':
    conn = boto.s3.connect_to_region(BUCKET_LOCATION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_ACCESS_KEY_SECRET,
        calling_format=boto.s3.connection.OrdinaryCallingFormat()
    )
    _bucket = conn.get_bucket(bucket_name)
    args = sys.argv[1:]
    if not args:
        uploadFileNames = files_to_upload(sourceDir)
    else:
        uploadFileNames = args
    deploy(_bucket, uploadFileNames)
