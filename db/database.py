from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# 创建数据库连接引擎
engine = create_engine('mysql+pymysql://用户名:密码@host:port/数据库名', echo=True)

# 创建会话工厂和 scoped_session
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
