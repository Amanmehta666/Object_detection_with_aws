import boto3
import json

# specify your AWS credentials
access_key = ''
secret_key = ''
region_name = ''

# initialize the session and client
session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region_name
)
s3_client = session.client('s3')

# specify the S3 bucket and video file name
bucket_name = ''
video_file = 'videoplayback.mp4'

# initialize the Rekognition client
rekognition_client = session.client('rekognition')

# specify the S3 bucket and video file
video = {
    'S3Object': {
        'Bucket': bucket_name,
        'Name': video_file
    }
}

# specify the parameters for the face detection operation
response = rekognition_client.start_face_detection(
    Video=video,
    FaceAttributes='ALL'
)

# retrieve the job ID for the face detection operation
job_id = response['JobId']

# wait for the operation to complete
while True:
    response = rekognition_client.get_face_detection(
        JobId=job_id,
        MaxResults=1000
    )
    status = response['JobStatus']
    if status == 'SUCCEEDED':
        break
    elif status == 'FAILED':
        raise Exception('Face detection failed')

# print out the detected faces
for face_detection in response['Faces']:
    print(json.dumps(face_detection, indent=4))