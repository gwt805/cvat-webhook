<div align="center">
    <img src="./webhooks-banner.svg">
</div>

# 环境
    cvat server: 2.4.1
    python >= 3.9
    pip install -r requirements.txt
# 说明
- 入口文件: `main.py`

- 配置文件: `config/config.py`

- 根据cvat webhook 中 `event` 分类然后手动解析字段并转发
    - [点我查看具体字段信息](./docs/field_info.md)

- 如果要改变 `config/config.py` 中的端口, 则 `docker-compose.yml` 文件也需同步改

- `docker logs -f 容器id` # 查看容器日志

- 如有其他问题请联系我, Q : `1973735972`

# 运行
- 先配置 `config/config.py` 文件

- 第一种: `python main.py`

- 第二种: `docker-compose up`, 如果运行不报错的话，再加一个 `-d`