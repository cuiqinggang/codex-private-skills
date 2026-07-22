下面是可以直接放进 GitHub 的说明书草稿，文件名建议：

`SPEC_KIT/UF-引擎接口说明书_Engine-Interface_v1.0.md`

你可以整段复制保存。后面要改版本号，我们再出 v1.1、v2.0。

---

# UF-引擎接口说明书 · Engine-Interface_v1.0

（UltraFusion-MVE 系列 · 引擎插座规范）

> 文件路径建议：`UltraFusion-SpecKit/SPEC_KIT/UF-引擎接口说明书_Engine-Interface_v1.0.md`
> 适用范围：MVE0 起步版本，一直到 UltraFusion A/B/C/D 全流程版本
> 目标：让底层“回答引擎”可以随时更换，而上层 UltraFusion 流程不用大改

---

## 1. 文档目的 · Purpose

本说明书定义 UltraFusion 项目中**“回答引擎（Engine）”的统一接口规范**，让你可以：

* 在不改前端、不改 V15、不改 A/B/C/D 流程的前提下，自由更换底层引擎：

  * 官方 API
  * 本地大模型
  * 自研浏览器自动化 / 爬虫引擎
  * 其它第三方服务
* 让所有上层逻辑只依赖一个稳定的函数：

  * 单引擎：`getAnswerFromEngine(question)`
  * 多引擎：`runEnginesForQuestion(question, engineIds[])`

**重点思想：**

> 上层 UltraFusion = 智慧层
> 底层 Engine = 可插拔的“发动机”
> 只要 Engine 接口不变，内部实现你可以随便换。

---

## 2. 名词约定 · Terminology

* **Engine（引擎）**
  一个可以接收“文本问题”，返回“文本答案”的黑盒组件。
  内部可以是 API、本地 LLM、自研爬虫等。

* **EngineId（引擎编号）**
  用一个字符串标识不同引擎，比如：

  * `"gpt_api"`
  * `"deepseek_api"`
  * `"grok_api"`
  * `"gemini_api"`
  * `"local_llm"`
  * `"custom_crawler_1"`

* **MVE0**
  UltraFusion 最小可用版本：

  * 只有一个前端页面
  * 一个后端 `server.js`
  * 一个统一入口 `getAnswerFromEngine(question)`

* **UltraFusion A/B/C/D 层**
  上层流程，负责多模型极限稿、融合、验证。
  本文只关心：它们**如何调用引擎，不关心引擎内部怎么做**。

---

## 3. 总体设计 · Overall Design

### 3.1 目标概述

Engine 接口要满足：

1. **最小要求（MVE0）**

   * 支持单一引擎
   * 后端提供 `/ask` HTTP 接口
   * 前端只关心：

     * 传一个问题
     * 拿回一个字符串答案

2. **未来扩展（支持多引擎）**

   * 可以扩展为同时调用多种引擎（GPT、DeepSeek、Grok、Gemini…）
   * 返回结构化结果，为 A/B/C 层融合提供原材料。

3. **实现可自由替换**

   * API / 本地模型 / 自研爬虫 均可
   * 但都要遵守同一个接口约定。

---

## 4. 单引擎接口规范（MVE0 必须）

### 4.1 后端核心函数签名 · Core Function

在 `backend/server.js` 中，必须存在一个统一入口函数：

```js
/**
 * UltraFusion MVE0 统一引擎入口
 * @param {string} question  用户输入的问题（纯文本）
 * @returns {Promise<string>} 引擎返回的答案（纯文本）
 */
async function getAnswerFromEngine(question) {
  // 内部实现由你自己决定：
  // - 可以调用 API
  // - 可以调用本地模型
  // - 也可以调用你自写的浏览器自动化/爬虫逻辑
}
```

上层 UltraFusion、前端、其它模块**只允许依赖这个函数**，不直接关心内部实现。

> 以后你想换引擎，只改这个函数内部即可。

---

### 4.2 输入约定 · Input Contract

`question` 字段要求：

* 类型：`string`
* 内容：用户的完整问题（已经在前端做过基本清洗即可）
* 推荐：前端已经 `.trim()`，后端可以再安全检查一次：

  * 去掉首尾空格
  * 如果为空，直接返回提示信息

示例（后端安全处理）：

```js
const raw = req.body.question || "";
const question = raw.trim();
if (!question) {
  return res.json({ answer: "【提示】你还没有输入问题。" });
}
```

---

### 4.3 输出约定 · Output Contract

`getAnswerFromEngine(question)` 必须返回：

* 类型：`Promise<string>`
* 内容：纯文本答案，可以包含换行、Markdown（由你决定）

错误处理规范：

1. **正常情况**：返回“逻辑上的成功答案”字符串
2. **内部出错但可恢复**：

   * 返回一个带有前缀的提示，比如：

     ```text
     【临时错误】调用引擎失败，请稍后重试。
     ```
3. **真正抛异常**：由外层 `try/catch` 捕获，并返回统一错误文案：

```js
app.post("/ask", async (req, res) => {
  try {
    const question = (req.body.question || "").trim();
    if (!question) {
      return res.json({ answer: "【提示】你还没有输入问题。" });
    }

    const answer = await getAnswerFromEngine(question);
    res.json({ answer });
  } catch (err) {
    console.error("Engine error:", err);
    res.status(500).json({ answer: "【系统错误】后端处理失败，请稍后重试。" });
  }
});
```

> 约束：**不要让异常直接炸掉 Node.js 进程**，所有错误都要被包在一个“可控的字符串答案”里。

---

## 5. HTTP 层接口规范 · HTTP API Contract（MVE0）

前端与后端之间的协议，在 MVE0 固定为：

### 5.1 请求 · Request

* Method：`POST`
* URL：`http://localhost:3000/ask`
* Header：`Content-Type: application/json`
* Body JSON：

```json
{
  "question": "用户输入的问题"
}
```

### 5.2 响应 · Response

成功时：

```json
{
  "answer": "这里是引擎返回的文本答案"
}
```

失败时（如后端 500）：

```json
{
  "answer": "【系统错误】后端处理失败，请稍后重试。"
}
```

> 说明：
>
> * 前端**只看 `answer` 字段**。
> * 如果以后要加元信息（引擎名字、耗时等），可以扩展为：
>
>   ```json
>   {
>     "answer": "...",
>     "engineId": "gpt_api",
>     "elapsedMs": 1234
>   }
>   ```
>
>   但 MVE0 版本前端可以先不依赖这些字段。

---

## 6. 多引擎扩展接口（为 A/B/C/D 做准备）

> 本节是预留给未来的 MVE1 / UltraFusion 完整版，MVE0 可以暂时不实现。

### 6.1 多引擎请求签名 · Multi-Engine Signature

建议在后端增加一个更通用的函数（不必马上实现）：

```js
/**
 * 同时向多个引擎提问，返回一个结果数组
 * @param {string} question
 * @param {string[]} engineIds  要调用的引擎列表
 * @returns {Promise<EngineResult[]>}
 */
async function runEnginesForQuestion(question, engineIds) {
  // 内部可以并行调用各个引擎
}
```

配套类型定义（伪代码 / TypeScript 风格）：

```ts
type EngineId =
  | "gpt_api"
  | "deepseek_api"
  | "grok_api"
  | "gemini_api"
  | "local_llm"
  | string;

interface EngineResult {
  engineId: EngineId;
  ok: boolean;           // 是否调用成功
  answerText: string;    // 纯文本答案（给 V15 和融合层用）
  raw?: any;             // 原始返回（可选，用于调试、日志）
  error?: string;        // 若 ok=false，这里写错误信息
}
```

> 说明：
>
> * A 层 / B 层可以依赖 `EngineResult[]` 来做 V15 评审和融合。
> * 实际 HTTP 返回可以先不暴露这些细节，只在后端内部使用。

---

## 7. 引擎内部实现的自由度 · Implementation Flexibility

本说明书**故意不规定**引擎内部如何实现，只规定“接口长什么样”。

你可以自由选择：

* **API 型引擎**

  * 调用官方 API（OpenAI、DeepSeek、Grok、Gemini 等）
  * 或调用你自己的中转服务

* **本地模型引擎**

  * 通过 HTTP 调用本地运行的大模型服务（如 `http://127.0.0.1:8000/completion`）

* **浏览器自动化 / 爬虫引擎**

  * 使用你自己写的脚本，通过浏览器控制获取答案
  * 在本接口说明书中，只被视为一种“自研引擎实现”，不做细节展开

统一原则：

> 不管内部怎么做，对上层只暴露：
>
> * 输入：`question: string`
> * 输出：`answer: string`
>   其它细节全部封装。

---

## 8. 日志与调试建议 · Logging & Debugging

建议在引擎层保留最基本的日志能力，方便以后调试：

* 记录每次请求的：

  * 时间
  * EngineId
  * 问题长度 / 摘要
  * 调用耗时
  * 成功 or 失败

示例（极简控制台日志）：

```js
console.log(`[Engine] id=gpt_api, q="${question.slice(0, 30)}...", ok=${ok}, ms=${elapsedMs}`);
```

后期你可以将它升级为：

* 写入文件
* 写入数据库
* 用于 UltraFusion TESTS 目录的自动生成日志

---

## 9. 与 UltraFusion 文档的关系 · Doc Relationship

本说明书与其它文档的分工：

* `UltraFusion_Core_v1.0.md`

  * 描述：整体愿景、A/B/C/D 层结构、V15 的核心地位
  * 把 Engine 当作“黑盒”

* `UltraFusion_Phase0_RUNBOOK_v2.0.md`

  * 描述：Phase 0 手工操作流程（包含 Router、D-Lite 等）
  * 可以引用本说明书中关于 `/ask` 接口、`getAnswerFromEngine` 的规范

* **本文件：`UF-引擎接口说明书_Engine-Interface_v1.0.md`**

  * 专门说明：

    * 底层引擎接口
    * 前后端之间的 HTTP 协议
    * 单引擎 / 多引擎调用形式
  * 不写任何特定平台的实现细节。

---

## 10. 版本策略 · Versioning

当前版本：`Engine-Interface_v1.0`

未来如有以下变更，建议升级版本号并在顶部写清差异：

* 增加多引擎 HTTP 接口（例如 `/ask_multi`）
* 增加流式输出（Streaming）
* 增加结构化答案格式（例如同时返回 SVO 原子事实草稿）
* 增加与 UltraFusion A/B/C/D 层的直接对接规范

版本命名建议：

* `Engine-Interface_v1.1`：小修改（补充字段、澄清语义）
* `Engine-Interface_v2.0`：大改动（协议结构变更）

---

## 11. 一句话总结

> **底层引擎可以随时换，
> 上层 UltraFusion 永远只认：
> `getAnswerFromEngine(question) → answer`
> 以及未来的 `runEnginesForQuestion(question, engineIds[]) → EngineResult[]`。**

只要遵守这份说明书，你就可以：

* 先用一个临时引擎把系统跑起来
* 再慢慢换成你心目中“更极限”的引擎实现
* 而不需要推倒重来。

---

如果你愿意，下一步我们可以：

* 把这份说明书里提到的接口，
  写进一个真正的 `server.js` 模板版本：

  * 保留空的 `getAnswerFromEngine` 实现
  * 并在代码注释里标出：

    * “这里可以接 API”
    * “这里可以接你的自研引擎”

你只要一句话，比如：

> “按这个接口说明，给我一个对应的 server.js 模板。”

我就给你一份可以直接丢进 `backend/server.js` 使用的“引擎插座版”后端。
2025.12.10
