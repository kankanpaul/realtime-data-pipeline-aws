import json
import base64

def lambda_handler(event, context):
    output = []

    for record in event['records']:
        try:
            # Decode the base64 data
            payload = base64.b64decode(record['data']).decode('utf-8')
            stream_record = json.loads(payload)

            # Extract fields if eventName is INSERT
            if stream_record.get('eventName') == 'INSERT':
                new_image = stream_record.get('dynamodb', {}).get('NewImage', {})

                user_data = {
                    'id': new_image['id']['S'],
                    'name': new_image['name']['S'],
                    'email': new_image['email']['S'],
                    'phone_number': new_image['phone_number']['S'],
                    'created_at': new_image['created_at']['S'],
                    'age': int(new_image['age']['N']),
                    'address': new_image['address']['S'],
                }

                # Convert to newline-delimited JSON line
                transformed_payload = json.dumps(user_data) + '\n'
                result_status = 'Ok'
            else:
                # If not an INSERT, skip but return as Ok
                transformed_payload = ''
                result_status = 'Dropped'

        except Exception as e:
            # In case of parsing error, retain original data
            transformed_payload = payload + '\n'  # Still line-delimited
            result_status = 'ProcessingFailed'

        # Append transformed record to output list
        output.append({
            'recordId': record['recordId'],
            'result': result_status,
            'data': base64.b64encode(transformed_payload.encode('utf-8')).decode('utf-8')
        })

    return {'records': output}
