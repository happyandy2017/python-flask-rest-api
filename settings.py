from flask import Flask
import os

basedir= os.path.abspath(os.path.dirname(__file__)) #获取当前文件的绝对路径

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///'+ os.path.join(basedir,'database.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False















