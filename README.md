# 联系人后端

本项目是一个联系人管理系统的后端部分，使用 Flask 框架和 SQLite 数据库实现。它提供了基本的增、删、改、查功能。

## 功能

- **获取所有联系人**: `GET /contacts`
- **添加联系人**: `POST /contacts`
- **修改联系人**: `PUT /contacts/<id>`
- **删除联系人**: `DELETE /contacts/<id>`
- **查找联系人**: `GET /contacts/search?name=<name>`

## 使用
- **运行Flask应用程序**
- **后端将在 http://127.0.0.1:5000 上运行**

## 数据库
- **本项目使用 SQLite 数据库，数据存储在 contacts.db 文件中。可以使用 DB Browser for SQLite 等工具查看和管理数据库**
