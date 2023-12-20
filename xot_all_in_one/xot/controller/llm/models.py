# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import os
import openai
import backoff 
import requests
import time

completion_tokens = prompt_tokens = 0
openai.api_key = os.getenv("OPENAI_API_KEY")


def chatgpt(prompt, instruct=None, model="", temperature=0.0, max_tokens=1000, n=1, stop=None) -> list:
    if instruct is not None:
        messages = [{"role": "system", "content": instruct}, {"role": "user", "content": prompt}]
    else:
        messages = [{"role": "user", "content": prompt}]
    return gpt(messages, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)


def get_oai_completion(messages, model, temperature, max_tokens, cnt=1, stop=None):
    try: 
        res = openai.ChatCompletion.create(
        engine=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        n=cnt,
        stop=stop)
    
        return res

    except requests.exceptions.Timeout:
        # Handle the timeout error here
        print("The OpenAI API request timed out. Please try again later.")
        return None
    except openai.error.InvalidRequestError as e:
        # Handle the invalid request error here
        print("The OpenAI API request was invalid:%s"%e)
        return None
    except openai.error.APIError as e:
        if "The operation was timeout" in str(e):
            # Handle the timeout error here
            print("The OpenAI API request timed out. Please try again later.")
            time.sleep(3)
            return get_oai_completion(messages, model, temperature, max_tokens, cnt, stop)          
        else:
            # Handle other API errors here
            print("The OpenAI API returned an error:%s"%e)
            return None
    except openai.error.RateLimitError as e:
            print("RateLimitError. Please try again later.")
            time.sleep(3)
            return get_oai_completion(messages, model, temperature, max_tokens, cnt, stop)
    except openai.error.ServiceUnavailableError as e:
            return get_oai_completion(messages, model, temperature, max_tokens, cnt, stop)



def gpt(messages, model, temperature, max_tokens, n, stop=None) -> list:
    global completion_tokens, prompt_tokens
    outputs = []
    
    res = get_oai_completion(messages, model, temperature, max_tokens, n, stop)

    outputs.extend([choice["message"]["content"] for choice in res["choices"]])
    # log completion tokens
    completion_tokens += res["usage"]["completion_tokens"]
    prompt_tokens += res["usage"]["prompt_tokens"]
    
    return outputs
 
