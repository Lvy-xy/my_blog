# Docker 化的 Markdown 博客

一个轻量级的 Flask 应用，用于在容器内上传并查看 Markdown 文件和图片。上传的 Markdown 可以在浏览器中即时渲染，同时图片通过同一容器的静态资源路径提供。

## 功能
- 上传 Markdown（`.md`、`.markdown`）及常见图片（`.png`、`.jpg`、`.jpeg`、`.gif`、`.svg`）。
- 列出所有已上传的 Markdown 文件。
- 在线渲染并查看 Markdown，支持代码块、表格和目录。
- 下载原始 Markdown 文件。

## 本地构建与运行
1. 构建镜像：
   ```bash
   docker build -t my-blog .
   ```
2. 运行容器并挂载本地数据目录（用于持久化上传文件）：
   ```bash
   docker run -d \
     -p 8000:8000 \
     -v $(pwd)/data:/app/data \
     --name my-blog \
     my-blog
   ```
   - 默认上传目录：`/app/data/uploads`。
   - 可通过环境变量 `UPLOAD_DIR` 修改上传目录位置。

3. 打开浏览器访问 `http://<服务器IP>:8000`，即可上传和查看文件。

## 环境变量
- `PORT`：应用监听端口，默认为 `8000`。
- `UPLOAD_DIR`：上传文件保存路径，默认为 `/app/data/uploads`。
- `SECRET_KEY`：Flask 的会话密钥，如需生产环境部署请自行设置更安全的值。

## 手动运行（非容器）
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
然后访问 `http://127.0.0.1:8000`。

## 使用建议
- 建议将 `data/` 目录挂载到宿主机以持久化上传文件。
- 可以在反向代理（如 Nginx）前面增加 HTTPS 支持，保障上传内容安全。
