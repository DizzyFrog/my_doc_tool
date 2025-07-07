from dotenv import load_dotenv
import os
load_dotenv('.env')
from openai import OpenAI

class AIClient:
    def __init__(self):
        self._init_client()
    
    def _init_client(self):
        """使用最新配置初始化客户端"""
        api_key = os.getenv('APIKEY')
        base_url = os.getenv('BASEURL')
        model = os.getenv('MODEL_NAME')
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model

    def get_response_with_tongyi(self, prompt):
        # 确保每次使用最新配置
        self._init_client()
        
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {'role': 'system', 'content': '你是亚信安全公司的软件需求工程师，负责需求分析'},
                {'role': 'user', 'content': prompt}
            ]
        )
        return completion.choices[0].message.content

aiclient = AIClient()

if __name__ == "__main__":
    print(aiclient.get_response_with_tongyi("你好"))