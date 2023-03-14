import openai

def buildmodel(question):
    #fetching api key 
    # https://platform.openai.com/account/api-keys
    # 
    openai.api_key = ('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')

    #Building engine
    request = openai.Completion.create(
        model="text-davinci-001",
        prompt=question,
        temperature=0.4,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    res = request["choices"][0]
    print(res['text'])
    result=res['text']
    return result