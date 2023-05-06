import boto3

# Initialize the client with your AWS access key, secret key, and region
client = boto3.client('transcribe', 
                      aws_access_key_id='your_access_id', 
                      aws_secret_access_key='your_secret_key', 
                      region_name='ypur_region')

# Specify the S3 bucket and file name of the audio file
bucket = 'your_bucket_name'
audio_file = 'audio.p3'

# Call the StartTranscriptionJob API to transcribe the audio
response = client.start_transcription_job( 
    TranscriptionJobName='audio-transcription-job-1',
    LanguageCode='en-US',
    Media={
        'MediaFileUri': f's3://{bucket}/{audio_file}'
    },
    OutputBucketName='your bucket'
)

# Get the job ID from the response
job_id = response['TranscriptionJob']['TranscriptionJobName']

# Wait for the job to complete
while True:
    job_response = client.get_transcription_job(TranscriptionJobName=job_id)
    status = job_response['TranscriptionJob']['TranscriptionJobStatus']
    if status == 'COMPLETED' or status == 'FAILED':
        break

# Get the transcript from the output S3 bucket
transcript_file = job_response['TranscriptionJob']['Transcript']['TranscriptFileUri']
s3 = boto3.client('s3')
transcript = s3.get_object(Bucket='your-output-bucket-name', Key=transcript_file.split('/')[-1])['Body'].read().decode('utf-8')

# Print the transcript
print(transcript)