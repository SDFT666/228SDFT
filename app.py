# -*- coding: utf-8 -*-
"""
文表领航Navigator · 后端 Mock 服务
----------------------------------
岗位：前端演示 & 部署工程师模块
作用：为前端 (index.html) 提供调试用的模拟接口，不接入真实 AI / RAG。
启动：python app.py  （默认监听 127.0.0.1:5000）
依赖：flask、flask-cors
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 开启跨域，允许前端通过浏览器直接访问本服务


@app.route('/upload', methods=['POST'])
def upload():
    """文件上传接口（Mock）

    接收字段：files（多文件，form-data）
    行为：仅打印文件名，不做真实落盘与解析。
    TODO: 后续对接【岗位3 · RAG 模块】——
          将上传文件解析、切片、向量化并写入知识库，供 Agent 检索使用。
    """
    files = request.files.getlist('files')
    if not files:
        return jsonify({"code": 1, "message": "未收到任何文件"}), 400

    names = []
    for f in files:
        # 读取一次拿大小，再 seek 回起点，方便后续真实落盘
        data = f.read()
        size = len(data)
        f.stream.seek(0)
        names.append(f.filename)
        print(f"[UPLOAD] 收到文件: {f.filename} | 大小: {size} bytes")

    # TODO: 调用 RAG 模块完成文档解析 + 向量入库
    return jsonify({
        "code": 0,
        "message": "上传成功",
        "count": len(names),
        "files": names
    })


@app.route('/chat', methods=['POST'])
def chat():
    """问答接口（Mock）

    接收 JSON: { "project_id": str, "question": str }
    返回: { "code": 0, "markdown": str }  其中 markdown 为内置模拟表格，
          用于调试前端 marked.js 渲染。
    TODO: 后续对接【岗位2 · Agent 模块】——
          由 Agent 编排 RAG 检索结果 + LLM 生成真实回答，再返回 markdown。
    """
    data = request.get_json(silent=True) or {}
    project_id = data.get('project_id', '')
    question = data.get('question', '')
    print(f"[CHAT] project_id={project_id!r} | question={question!r}")

    # TODO: 调用 Agent 模块，传入 project_id 与 question，获取真实结果
    md = (
        "## 模拟回答（调试用）\n\n"
        f"> 项目编号：`{project_id}`\n>\n"
        f"> 提问：{question}\n\n"
        "### 项目进度概览\n\n"
        "| 阶段 | 状态 | 负责人 | 完成度 |\n"
        "| :--- | :---: | :---: | :---: |\n"
        "| 需求调研 | ✅ 已完成 | 张三 | 100% |\n"
        "| 方案设计 | ✅ 已完成 | 李四 | 100% |\n"
        "| 开发实现 | 🔄 进行中 | 王五 | 60% |\n"
        "| 测试验收 | ⏳ 待开始 | 赵六 | 0% |\n"
        "| 上线部署 | ⏳ 待开始 | 钱七 | 0% |\n\n"
        "### 关键风险\n\n"
        "| 风险项 | 等级 | 应对措施 |\n"
        "| :--- | :---: | :--- |\n"
        "| 接口联调延迟 | 高 | 提前约定接口契约，并行开发 |\n"
        "| 数据质量不足 | 中 | 补充标注数据，引入校验规则 |\n"
        "| 进度汇报滞后 | 低 | 每日站会同步，周报留痕 |\n"
    )

    return jsonify({
        "code": 0,
        "message": "ok",
        "markdown": md
    })


if __name__ == '__main__':
    # 端口 5000，开启 debug 便于调试（生产环境请关闭 debug 并使用 WSGI 服务器）
    app.run(host='127.0.0.1', port=5000, debug=True)