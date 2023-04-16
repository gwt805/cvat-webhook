<div align="center">
    <img src="./webhooks-banner.svg">
</div>

# 环境
    cvat server: 2.4.1
    python >= 3.8
    pip install -r requirements.txt
# 说明
- 入口文件: `main.py`

- 配置文件: `config/config.py`

- 根据cvat webhook 中 `event` 分类然后手动解析字段并转发
    - [点我查看具体字段信息](./docs/field_info.md)

- 如有其他问题请联系我, Q : `1973735972`