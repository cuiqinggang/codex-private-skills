// ================================
// UltraFusion MVE0 后端（占位版）
// 不写具体爬虫，只预留统一入口
// ================================

// 1. 引入依赖（目前只需要 express）
const express = require("express");

// 2. 创建应用
const app = express();
const PORT = 3000;

// 3. 允许前端网页（本地 file:// 或将来托管的网页）访问这个后端
app.use((req, res, next) => {
  // 允许任何来源访问（本地开发方便）
  res.header("Access-Control-Allow-Origin", "*");
  // 允许的自定义请求头
  res.header(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested-With, Content-Type, Accept"
  );
  // 允许的请求方法
  res.header("Access-Control-Allow-Methods", "GET, POST, OPTIONS");

  // 处理预检请求（OPTIONS），直接放行
  if (req.method === "OPTIONS") {
    return res.sendStatus(200);
  }

  next();
});

// 4. 解析 JSON 请求体（前端会以 JSON 形式 POST 问题过来）
app.use(express.json());

/**
 * 5. 核心占位函数：统一的“答案引擎入口”
 *
 *   以后你无论用：
 *   - 爬虫 / Playwright / 别的浏览器自动化
 *   - 某个 API（OpenAI / DeepSeek ……）
 *   - 本地大模型 / 其他服务
 *
 *   都只需要在这里面实现真正的逻辑，
 *   保证最终 return 一个字符串 answer 即可。
 *
 *   现在先返回一个“本地测试假答案”，证明整条链路是通的。
 */
async function getAnswerFromEngine(question) {
  // TODO：这里以后改成“真正的引擎逻辑”

  const fakeAnswer =
    `【本地测试】后端已经收到你的问题：\n\n` +
    `${question}\n\n` +
    `（这里以后会换成你自己的“真正回答”（比如爬虫抓回来的结果））`;

  return fakeAnswer;
}

// 6. 接收前端发送的问题，然后调用统一引擎
app.post("/ask", async (req, res) => {
  try {
    const question = (req.body.question || "").trim();

    // 没有输入问题的情况
    if (!question) {
      return res.json({
        answer: "【本地提示】你还没有输入问题。",
      });
    }

    console.log("收到前端问题：", question);

    // ▶▶ 关键：这里调用你上面的“答案引擎入口”
    const answer = await getAnswerFromEngine(question);

    // 把答案以 JSON 的形式返回给前端
    return res.json({ answer });
  } catch (err) {
    console.error("处理 /ask 时发生错误：", err);
    return res.status(500).json({
      answer: "【本地错误】后端处理时出错了，请稍后再试。",
    });
  }
});

// 7. 简单健康检查接口（可选）
app.get("/", (req, res) => {
  res.send("UltraFusion MVE0 backend is running.");
});

// 8. 启动后端服务
app.listen(PORT, () => {
  console.log(`后端启动成功：http://localhost:${PORT}/`);
});
