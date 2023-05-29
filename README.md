# DataAsset-Generator
基于AI和文档的大规模数据集生成和验证工具｜ChatGLM、 P-Tuning v2、ChatGPT
![homepage.png](https://github.com/Markz1122/DataAsset-Generator/blob/main/homepage.png)

## 介绍
工具目标主要集中在主流大模型微调数据集样本的生成方面，偏重利用文档生成我们希望领域的问答数据集。
目前，实际应用于ChatGLM-6B + P-Tuning v2框架的优化微调场景，文档来自大量包含语料内容的TXT文档，通过提示词和ChatGPT-3生成相关问答指令样本，并导出为微调框架可直接利用的训练文件。

## 使用方法
整体流程分为五步：
1. GPT参数设置：设置GPT类型、GPT API KEY、GPT提示词
2. 文档上传和解析设置：上传文档、设置文档分段字数（字数范围内，以最后一个句号为分段后的内容结尾）
3. 文档解析结果展示：展示分段后的文档内容、切换上下文段
4. 样本生成参数设置和结果展示：设置生成的问题数量、链接GPT根据提示词生成问答样本
5. 导出样本集：缓存当前文段生成问答样本、导出当前工作缓存的所有问答数据集为训练文件、下载导出的训练文件
有些步骤可单独使用或组合使用。
![homepage-introduction.png](https://github.com/Markz1122/DataAsset-Generator/blob/main/homepage-introduction.png)

## 待改进
1. 模块1 仅支持ChatGPT-3.5，即将支持ChatGPT-4和本地化部署ChatGLM，未来支持更多大模型框架
2. 模块2 仅支持txt，即将支持docx，未来支持xlsx、pptx等格式（需结合相关nlp和文档解析框架）
3. 模块4 样本生成结果全搬GPT回答，未来支持提取GPT回答结果中的问答内容并结构化
4. 整体 确少异常校验，未来需提高整体可用性和交互性
