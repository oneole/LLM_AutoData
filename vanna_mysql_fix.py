import os
import pymysql
from dotenv import load_dotenv
import requests

load_dotenv()

class DeepSeekVanna:
    def __init__(self):
        # 检查环境变量是否加载成功
        required_envs = ["DEEPSEEK_API_KEY", "DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
        for env in required_envs:
            if not os.getenv(env):
                raise ValueError(f"Missing required environment variable: {env}")
        
        # MySQL连接配置
        self.mysql_config = {
            "host": os.getenv("DB_HOST"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME"),
            "cursorclass": pymysql.cursors.DictCursor,
            "charset": "utf8mb4"
        }
        
        # 本地知识库
        self._ddls = []
        self._examples = []

    def train(self, ddl=None, question=None, sql=None):
        """存储训练数据"""
        if ddl: 
            self._ddls.append(ddl)
        if question and sql:
            self._examples.append((question, sql))

    def _get_connection(self):
        """获取MySQL连接"""
        return pymysql.connect(**self.mysql_config)

    def generate_sql(self, question: str) -> str:
        """调用DeepSeek API生成SQL"""
        # 使用字符串拼接而不是多行f-string
        db_structs = "".join(self._ddls)
        example_queries = ""
        for q, s in self._examples:
            example_queries += f"问题: {q}\nSQL: {s};\n"
        
        prompt = "根据以下数据库结构和示例，生成MySQL查询语句:\n\n"
        prompt += f"数据库结构:\n{db_structs}\n\n"
        prompt += f"示例查询:\n{example_queries}\n"
        prompt += f"新问题: {question}\n"
        prompt += "要求: 只输出MySQL语法SQL，不要包含任何解释"
        
        headers = {
            "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1  # 降低随机性以保证SQL准确性
        }
        
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            raw_sql = response.json()["choices"][0]["message"]["content"]
            
            # 提取SQL代码块（如果有）
            if "```sql" in raw_sql:
                return raw_sql.split("```sql")[1].split("```")[0].strip()
            return raw_sql.strip().strip(';') + ';'  # 确保结尾有分号
        except Exception as e:
            raise RuntimeError(f"API调用失败: {str(e)}")

    def execute_sql(self, sql: str):
        """执行SQL并返回结果"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    return cursor.fetchall()
        except pymysql.Error as e:
            raise RuntimeError(f"数据库执行错误: {e}") 