from http import HTTPStatus
import dashscope

dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'

def call_with_stream():
    messages = [
        {'role': 'user', 'content': 'Introduce the capital of China'}]
    output_data = []
    
    responses = dashscope.Generation.call("qwen-max",
                                messages=messages,
                                result_format='message',  # set the result to be "message"  format.
                                stream=True, # set streaming output
                                incremental_output=True  # get streaming output incrementally
                                )
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            content = response.output.choices[0]['message']['content']
            print(content, end='')  # Still prints to console
            output_data.append({'content': content})  # Append to JSON-compatible list
        else:
            error_info = {
                'request_id': response.request_id,
                'status_code': response.status_code,
                'error_code': response.code,
                'error_message': response.message
            }
            output_data.append({'error': error_info})
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
            
    # Convert the output data to JSON format and print it
    json_output = json.dumps(output_data, indent=4)
    print("\nJSON Output:\n", json_output)
            
if __name__ == '__main__':
    call_with_stream()