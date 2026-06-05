# G17 Xiaolongxia-style Short Reply Dry-run

| Model | S | HTTP | Natural | Short | No false promise | No model leak | Parent group | Latency ms | Grade | Preview |
| --- | ---: | ---: | --- | --- | --- | --- | --- | ---: | --- | --- |
| `meta/llama-3.1-8b-instruct` | 1 | 200 | true | true | true | true | true | 698 | A | "哈哈，当然是免费的！你可以先试试我们的辅导服务，了解一下我们的风格和方式。之后如果你觉得有用的话，我们可以继续合作。我们希望能帮助你解决问题和提高学习效率。" |
| `meta/llama-3.1-8b-instruct` | 2 | 200 | true | false | true | true | false | 1070 | B | 孩子成绩差，AI 可以帮助的确实有很多。首先，AI 可以帮助孩子讲解题目，找出他们不理解的部分，提高学习效率。其次，AI 可以帮助孩子改写作文，纠正语法和表达方式，提高写作水平。最后，AI 可以帮助孩子练习题目，模拟考试环境，提高孩子的应对能力。这些都是 AI 在学习中的小小助手，帮助孩子更好地学习和提高。 |
| `meta/llama-3.1-8b-instruct` | 3 | 200 | true | false | true | true | false | 1026 | B | 当然可以！我们提供了一个手机端的问答系统，方便您随时随地提问。您可以下载我们的手机应用程序，或者直接在手机浏览器中访问我们的网站，进行问答。我们会尽量降低门槛，帮助您轻松地获取所需的信息。您可以通过手机发送消息或发表评论，和我们交流。我们会尽量帮助您解决问题。 |
| `nvidia/nemotron-3-super-120b-a12b` | 1 | 200 | true | false | true | false | false | 15934 | C | We need to answer in Chinese, short, 60-100 characters, like a real person in a parent group, highlighting free trial, not too official, no mention of API, model, provider, not self-identifying as ChatGPT. Must be 60-100 |
| `nvidia/nemotron-3-super-120b-a12b` | 2 | 200 | true | false | true | false | false | 15539 | C | We need to respond in Chinese, short answer 60-100 characters (Chinese characters). Must be like a real person in a parent group, short, not exaggerating, not promising grade improvement, emphasize explaining problems, c |
| `nvidia/nemotron-3-super-120b-a12b` | 3 | 200 | true | false | true | false | false | 17195 | C | We need to respond in Chinese, like a real person in a parent group, short answer 60-100 characters, explain can use phone, lower barrier. No mention of API, model, provider. Must be 60-100 Chinese characters (including  |
| `meta/llama-3.1-70b-instruct` | 1 | 200 | true | true | true | true | true | 6326 | A | “大家好！我们的AI辅导服务目前是免费的，你们可以先让孩子试用一下，体验一下效果。我们会根据孩子的学习情况提供个性化的辅导和反馈。目前我们还在不断完善和改进服务，所以暂时不收费。欢迎大家试用和反馈，我们会尽力提供更好的服务。” |
| `meta/llama-3.1-70b-instruct` | 2 | 200 | true | false | false | true | false | 6770 | C | 孩子成绩差，确实需要关注。AI 可以作为辅助工具，帮助孩子提高成绩。它可以提供个性化的讲题服务，帮助孩子理解难点。同时，AI 还可以帮助孩子改作文，提高写作能力。另外，AI 也可以陪伴孩子练习，提供实时反馈和鼓励。虽然不能保证成绩一定提升，但 AI 的辅助确实可以让孩子的学习更高效和有趣。 |
| `meta/llama-3.1-70b-instruct` | 3 | 200 | true | true | true | true | true | 4786 | A | 当然可以！我们的服务完全支持手机使用。你可以直接在手机上打开对话框，输入你的问题或需求，我会尽快回复你。无论你是使用电脑还是手机，我们都希望为你提供便捷的服务。所以，不用担心电脑的问题，直接用手机问就好了！ |

Status: `G17_PARTIAL_XIAOLONGXIA_STYLE`
