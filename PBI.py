import boto3
import json

bedrock_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-2')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        user_question = body.get('question', '')

        response = bedrock_runtime.retrieve_and_generate(
            input={'text': user_question},
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': 'KBID',
                    'modelArn': 'arn:aws:bedrock:us-east-2::foundation-model/meta.llama3-3-70b-instruct-v1:0',
                    'generationConfiguration': {
                        'inferenceConfig': {
                            'textInferenceConfig': {
                                'temperature': 0.7,
                                'topP': 0.9,
                                'maxTokens': 512
                            }
                        }
                    }
                }
            }
        )

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': 'POST'
            },
            'body': json.dumps({'answer': response['output']['text']})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # ✅ Add CORS headers in error too
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': 'POST'
            },
            'body': json.dumps({'error': 'Internal server error', 'details': str(e)})
        }
