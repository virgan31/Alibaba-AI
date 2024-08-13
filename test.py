import random
from http import HTTPStatus
import dashscope

dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'

def call_stream_with_messages():
    messages = [
        {'role': 'user', 'content': 'Introduce the capital of China'}]
    responses = dashscope.Generation.call(
        'qwen1.5-7b-chat',
        messages=messages,
        seed=random.randint(1, 10000),  # set the random seed, optional, default to 1234 if not set
        result_format='message',  # set the result to be "message"  format.
        stream=True,
        output_in_full=True  # get streaming output incrementally
    )
    full_content = ''
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            full_content += response.output.choices[0]['message']['content']
            print(response)
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
    print('Full content: \n' + full_content)


if __name__ == '__main__':
    call_stream_with_messages()