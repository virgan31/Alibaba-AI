from http import HTTPStatus
import dashscope
import json

dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'

def call_with_stream():
    # Get the message content from manual input
    user_input = input("Enter your message: ")
    
    messages = [
        {'role': 'user', 'content': user_input}]
    merged_content = ""
    
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
            merged_content += content
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
            
    # Prepare the final output in JSON format
    output_data = {'content': merged_content}
    json_output = json.dumps(output_data, indent=4)
    
    # Write the JSON output to a file named 'respond.json'
    with open('respond.json', 'w') as json_file:
        json_file.write(json_output)
    
    # Optional: Print confirmation or the path to the saved file
    print("\nJSON Output saved to 'respond.json'")
            
if __name__ == '__main__':
    call_with_stream()