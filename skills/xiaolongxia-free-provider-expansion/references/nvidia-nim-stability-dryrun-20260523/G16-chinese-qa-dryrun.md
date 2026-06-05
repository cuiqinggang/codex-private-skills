# G16 Chinese QA Dry-run

| Model | Q | HTTP | Chinese | Concise | Useful | No garbled | Group suitable | Latency ms | Grade | Preview |
| --- | ---: | ---: | --- | --- | --- | --- | --- | ---: | --- | --- |
| `meta/llama-3.1-8b-instruct` | 1 | 200 | true | true | true | true | true | 648 | A | 家长不用着急，孩子的写作文能力可以通过慢慢培养来提高。可以从简单的日常生活中开始，要求孩子描述自己的日常活动，例如早上起床、吃早餐、上学等。这样可以让孩子逐渐习惯写作文的形式和内容。 |
| `meta/llama-3.1-8b-instruct` | 2 | 200 | true | true | false | true | true | 588 | A | 这个 AI 辅导孩子学习的主要目的是帮助他们理解和掌握学科知识，提高学习效率和兴趣。通过与孩子的互动，AI 可以提供个性化的学习建议和辅导，帮助他们克服学习困难和缺点。 |
| `meta/llama-3.1-8b-instruct` | 3 | 200 | true | true | true | true | true | 608 | A | 我建议一步一步引导孩子解决数学应用题。这样可以帮助他们理解问题，培养分析和解决问题的能力。直接给答案可能会让孩子缺乏思考和学习的机会。通过一步一步的引导，孩子可以自己思考和解决问题，进而提高他们的数学能力和自信心。 |
| `nvidia/nemotron-3-super-120b-a12b` | 1 | 200 | false | false | true | true | false | 23238 | C | We need to give three sentences, Chinese, <=120 characters, colloquial, no long explanation, no self-reference, no English, no gibberish, no empty marketing. Provide a simple method. Must be three sentences. Count charac |
| `nvidia/nemotron-3-super-120b-a12b` | 2 | 200 | false | false | true | true | false | 14405 | C | We need to answer in Chinese, colloquial, under 80 characters, no self-reference as large language model, no English. Provide answer to question: "有人在群里问：你这个 AI 辅导孩子学习到底有什么用？" So answer: AI can help kids with explanation |
| `nvidia/nemotron-3-super-120b-a12b` | 3 | 200 | false | false | true | true | false | 10455 | C | We need to answer in Chinese, short, <=120 characters, oral style, no English. The question: "孩子数学应用题不会做，AI 应该直接给答案，还是一步一步引导？请简短回答。" So answer: better to guide step by step, not just give answer. Provide short response.  |
| `meta/llama-3.1-70b-instruct` | 1 | 200 | true | true | true | true | true | 4534 | A | 你可以先让孩子写一段简单的日记，描述他今天做了什么，遇到了什么有趣的事情。然后，逐步引导他写短篇故事，鼓励他使用自己的想象力。同时，多给他提供写作的机会和鼓励，慢慢地他就会养成写作的习惯和兴趣。 |
| `meta/llama-3.1-70b-instruct` | 2 | 200 | true | true | true | true | true | 3109 | A | 我可以帮助孩子们查找资料、解答问题、纠正作业错误、提供学习建议和方法，还可以陪伴他们做练习题，甚至可以和他们讨论学习中的困难和兴趣。总的来说，我可以成为孩子们学习上的小助手和学习伙伴。 |
| `meta/llama-3.1-70b-instruct` | 3 | 200 | true | true | true | true | true | 4536 | A | 我觉得一步一步引导更好。直接给答案可能会让孩子觉得很方便，但实际上他们并没有真正理解问题的解决方法。通过一步一步的引导，孩子可以了解问题的思维过程，提高自己的数学思维能力和解决问题的能力。同时，也可以帮助孩子培养独立思考和解决问题的能力。 |

Status: `G16_PARTIAL_CHINESE_QA`
