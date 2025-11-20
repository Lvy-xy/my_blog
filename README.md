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

## 无法通过公网访问时的排查指南
- **确认端口映射**：容器需使用 `-p 8000:8000` 将容器端口映射到宿主机。使用 `docker ps` 或
  `docker inspect <容器名> -f '{{.HostConfig.PortBindings}}'` 检查端口是否正确映射。
- **在宿主机本地自检**：在服务器上运行 `curl http://127.0.0.1:8000/`，若能看到 HTML 返回说明容器正常，问题多半在网络层。
- **打开防火墙与安全组**：
  - 云厂商安全组需放行入站 TCP 8000。
  - 服务器自身若启用了防火墙（如 `ufw`/`firewalld`），需允许 8000 端口：`sudo ufw allow 8000/tcp` 或
    `sudo firewall-cmd --add-port=8000/tcp --permanent && sudo firewall-cmd --reload`。
- **检查宿主机端口占用**：`sudo ss -tlnp | grep :8000` 确保没有其他服务占用 8000 端口。
- **验证公网连通性**：从本地电脑使用 `telnet <公网IP> 8000` 或 `nc -vz <公网IP> 8000` 测试是否能打通；若打不通，说明流量被
  防火墙/安全组阻断或服务器未对外开放此端口。
- **使用反向代理场景**：若前面有 Nginx/负载均衡，需要确认其转发到宿主机 8000 端口，并根据需要将 `docker run` 的宿主机端口
  改为对外暴露的端口（如 `-p 80:8000`）。

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
