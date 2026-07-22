# 日用运行手册

## 先后顺序

1. 先确认 playwright-cli 可用：

playwright-cli --help

2. 打开网页：

playwright-cli open <url> --headed

3. 获取 snapshot：

playwright-cli snapshot --filename=<文件路径>

4. 根据 snapshot 找元素 ref。

5. 点击 / 填写 / 输入。

6. 再次 snapshot 确认页面变化。

7. 保存 screenshot。

8. 写 final-report.md。

## 失败恢复

如果 playwright-cli 不存在：

npm install -g @playwright/cli@latest

如果浏览器启动失败：

playwright-cli install-browser

如果 snapshot 没有目标元素：

1. 重新打开页面；
2. 等待页面加载；
3. 再执行 snapshot；
4. 仍失败则切换截图法或人工确认。

## 禁止盲目继续

以下情况必须停止：

1. 出现登录页；
2. 出现验证码；
3. 出现付款 / 删除 / 发布 / 发送按钮；
4. 页面要求真实账号权限；
5. 操作对象不明确。
