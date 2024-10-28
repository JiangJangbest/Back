from flask import Flask, request, jsonify  # 导入 Flask 和相关模块
from flask_sqlalchemy import SQLAlchemy  # 导入 SQLAlchemy 用于数据库操作

app = Flask(__name__)  # 创建 Flask 应用实例
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'  # 设置 SQLite 数据库路径
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁用对象修改追踪
db = SQLAlchemy(app)  # 创建 SQLAlchemy 数据库实例

# 定义联系人模型
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键 ID
    name = db.Column(db.String(80), nullable=False)  # 姓名字段
    phone = db.Column(db.String(20), nullable=False)  # 电话字段

# 初始化数据库
with app.app_context():
    db.create_all()  # 创建所有表

# 获取所有联系人
@app.route('/contacts', methods=['GET'])  # 定义 GET 请求的路由
def get_contacts():
    contacts = Contact.query.all()  # 查询所有联系人
    # 返回联系人列表，格式化为 JSON
    return jsonify([{'id': c.id, 'name': c.name, 'phone': c.phone} for c in contacts]), 200, {'Content-Type': 'application/json; charset=utf-8'}

# 添加联系人
@app.route('/contacts', methods=['POST'])  # 定义 POST 请求的路由
def add_contact():
    data = request.json  # 获取请求的 JSON 数据
    new_contact = Contact(name=data['name'], phone=data['phone'])  # 创建新联系人对象
    db.session.add(new_contact)  # 添加联系人到数据库会话
    db.session.commit()  # 提交会话以保存更改
    return jsonify({'message': 'Contact added successfully'})  # 返回成功消息

# 修改联系人
@app.route('/contacts/<int:id>', methods=['PUT'])  # 定义 PUT 请求的路由
def modify_contact(id):
    data = request.json  # 获取请求的 JSON 数据
    contact = Contact.query.get(id)  # 根据 ID 查询联系人
    if contact:
        contact.name = data['name']  # 更新联系人姓名
        contact.phone = data['phone']  # 更新联系人电话
        db.session.commit()  # 提交会话以保存更改
        return jsonify({'message': 'Contact updated successfully'})  # 返回成功消息
    return jsonify({'message': 'Contact not found'}), 404  # 返回未找到消息

# 查找联系人
@app.route('/contacts/search', methods=['GET'])  # 定义搜索联系人功能的路由，支持 GET 请求
def search_contacts():
    name = request.args.get('name')  # 从请求参数中获取要搜索的姓名
    # 使用 SQLAlchemy 查询，模糊匹配联系人姓名，使用 ilike 支持不区分大小写的匹配
    contacts = Contact.query.filter(Contact.name.ilike(f'%{name}%')).all()
    # 将查询到的联系人列表格式化为 JSON 返回
    return jsonify([{'id': c.id, 'name': c.name, 'phone': c.phone} for c in contacts]), 200, {'Content-Type': 'application/json; charset=utf-8'}


# 删除联系人
@app.route('/contacts/<int:id>', methods=['DELETE'])  # 定义 DELETE 请求的路由
def delete_contact(id):
    contact = Contact.query.get(id)  # 根据 ID 查询联系人
    if contact:
        db.session.delete(contact)  # 从数据库会话中删除联系人
        db.session.commit()  # 提交会话以保存更改
        return jsonify({'message': 'Contact deleted successfully'})  # 返回成功消息
    return jsonify({'message': 'Contact not found'}), 404  # 返回未找到消息

if __name__ == '__main__':
    app.run(debug=True)  # 启动 Flask 应用，启用调试模式
