import gradio as gr
import openai

contents = []
curIndexContent = 0
samples = None

def defDocHanle(doc, maxLength):
    contents.clear()
    global curIndexContent
    curIndexContent = 0
    global samples
    samples = None
    
    with open(doc.name, 'r') as f:
        suffixStr=''
        while True:
            content = f.read(int(maxLength-len(suffixStr)))
            if not content:
                break
            
            last_period_index = content.rfind('。')
            if last_period_index != -1:
                contents.append(suffixStr + content[:last_period_index + 1])# 包含最后一个句号
                suffixStr = content[last_period_index + 1:]
            else:
                contents.append(content)
                suffixStr=''
    f.close()
    
    
    samples = ['']*len(contents)
    return contents[0], ''

def defParaLast():
    global curIndexContent
    curIndexContent -= 1
    if curIndexContent < 0:
        curIndexContent = len(contents) - 1
    return contents[curIndexContent], samples[curIndexContent]
def defParaNext():
    global curIndexContent
    curIndexContent += 1
    if curIndexContent >= len(contents):
        curIndexContent = 0
    return contents[curIndexContent], samples[curIndexContent]

def defSampleGenerate(apiType, apiKey, apiTip, paraCur, sampleNum):
    question = apiTip + ", 生成" + str(int(sampleNum)) + "条样本，内容如下：\n“" + paraCur + "“"
    print("question:", question)
    if apiType == "ChatGPT3.5":
        openai.api_key = apiKey
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "user", "content": question},
            ],
        )
        print("answer:", chat_completion.choices[0].message.content)
        return chat_completion.choices[0].message.content
    else:
        return "暂不支持"+apiType
    
def defSampleCache(sampleResult):
    samples[curIndexContent] = sampleResult
    print(samples)
    return

def defSampleExport():
    with open("train.json", "w") as trainFile:
        for sample in samples:
            trainFile.write(sample + "\n")
    return "train.json"


with gr.Blocks() as demo:
    gr.HTML("""<h1 align="center">数据集生成工具</h1>""")
    gr.HTML("""<h3 align="center">一款基于AI和文档的大规模数据集生成和验证工具</h3>""")

    with gr.Row():
        with gr.Column(scale=1, min_width=300):
            apiType =  gr.Dropdown(choices=["ChatGLM-6B", "ChatGPT3.5", "ChatGPT4"], value="ChatGPT3.5",label="API 类型", interactive=True)
            apiKey = gr.Textbox(lines=1, placeholder="...",label="API KEY",interactive=True)
            # apiParam = gr.Textbox(lines=4, placeholder="...",label="API PARAMETOR")
            apiTip = gr.Textbox(lines=3, value="根据内容生成问答数据集，数据集样本的格式为json，每个样本格式严格按照{\"content\":\"问题\", \"summary\":\"答案\"}，且没有多余的内容",label="提示词", interactive=True)

            docUpload = gr.File(label="上传文档", file_types=[".txt"])
            docMaxSeg = gr.Number(lines=1, value="2048",label="文档最大分段字数", interactive=True)
            docHandle = gr.Button("处理文档")
        with gr.Column(scale=3):
            paraCur = gr.Textbox(lines=8, placeholder="...",label="当前处理文本")
            with gr.Row():
                paraLast = gr.Button("上一段")
                paraNext = gr.Button("下一段")

            sampleResult = gr.Textbox(lines=15, placeholder="...",label="问答样本生成结果")
            with gr.Row():
                sampleNum = gr.Number(lines=1, value="10", label="问答样本最大生成数量", interactive=True)
                sampleGenerate = gr.Button("生成问答")
                sampleCache = gr.Button("缓存样本")
                sampleExport = gr.Button("导出训练文件")
            sampleFile = gr.File(label="下载训练文件", file_types=[".txt"], interactive=False)
                
    docHandle.click(defDocHanle, [docUpload,docMaxSeg], [paraCur, sampleResult])
    
    paraLast.click(defParaLast, None, [paraCur,sampleResult])
    paraNext.click(defParaNext, None, [paraCur, sampleResult])
    
    sampleGenerate.click(defSampleGenerate, [apiType, apiKey, apiTip, paraCur, sampleNum], sampleResult)
    sampleCache.click(defSampleCache, [sampleResult], None)
    sampleExport.click(defSampleExport, None, sampleFile)
                
demo.launch()
