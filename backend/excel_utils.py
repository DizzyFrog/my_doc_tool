from collections import OrderedDict
import json
import pandas as pd
import os
from dotenv import load_dotenv
from mylog.log import logger
from pathlib import Path
from resource_util import resource_path

load_dotenv(resource_path('.env'),override=True)

class ExcelUtils:

    def __init__(self):
        self.sheet_name = os.getenv('SHEET_NAME')
        self.file_path = resource_path(os.getenv('FILE_PATH')) if os.getenv('FILE_PATH') else None
        self.df = None
        # json path = data/output/output.json
        self.columns = ['功能用户需求', '触发事件', '功能过程', '子过程描述', '数据组', '功能用户', '角色']
        self.output_json_path = resource_path(os.path.join('data', 'output', 'output.json'))


    def get_excel_sheets(self):
        try:
            xls = pd.ExcelFile(self.file_path)
            return xls.sheet_names
        except Exception as e:
            return [] 
        
    def _clean_text(self,text):
        """清理文本中的空白字符"""
        return str(text).strip().replace(" ", "").replace("\t", "").replace("\n", "")
        
    '''
    读取 .env配置的 excel 文件，封装为json
    '''
    def read_excel_to_pd(self) -> pd.DataFrame:
        """读取Excel为DataFrame"""
        if self.df is None:
            try:
                self.df = pd.read_excel(
                    self.file_path,
                    sheet_name=self.sheet_name,
                    header=0,
                    usecols=self.columns
                ).ffill()
                logger.info(f"读取excel成功: {self.file_path}, sheet: {self.sheet_name}, columns: {self.columns}")
            except Exception as e:
                logger.error(f"读取excel失败: {e}")
                raise
        return self.df
    
    def read_pd_to_json(self):
        result_list = []
        func_user_req_map = {}

        for _, row in self.df.iterrows():
            func_user_req = row['功能用户需求']
            func_process = row['功能过程']
            sub_processes = row['子过程描述']
            data_group = row['数据组']
            role = self._clean_text(row['角色']).replace("，",",")

            # 查找或创建功能用户需求对象
            if func_user_req not in func_user_req_map:
                user_req_obj = {
                    "功能用户需求": func_user_req,
                    "角色": role,
                    "功能过程": []
                }
                func_user_req_map[func_user_req] = user_req_obj
                result_list.append(user_req_obj)
            else:
                user_req_obj = func_user_req_map[func_user_req]

            # 查找或创建功能过程对象
            process_list = user_req_obj["功能过程"]
            process_obj = next((p for p in process_list if p["名称"] == func_process), None)
            if not process_obj:
                process_obj = {
                    "名称": func_process,
                    "子过程": [],
                    "数据组": []
                }
                process_list.append(process_obj)

            if sub_processes and sub_processes not in process_obj["子过程"]:
                process_obj["子过程"].append(sub_processes)
            if data_group and data_group not in process_obj["数据组"]:
                process_obj["数据组"].append(data_group)

        json_result = json.dumps(result_list, ensure_ascii=False, indent=4)
        os.makedirs(os.path.dirname(self.output_json_path), exist_ok=True)
        with open(self.output_json_path, 'w', encoding='utf-8') as file:
            file.write(json_result)
        logger.info("写入json成功")
        return json_result
    
    def check_info(self):
        """
        校验生成的JSON文件内容

        Args:
            json_path: JSON文件路径

        Returns:
            problems: 发现的问题列表
        """
        with open(self.output_json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        problems = []

        for item in data:
            func_user_req = item.get("功能用户需求", "")
            role_str = item.get("角色", "")
            # 支持中英文逗号
            roles = [r.strip() for r in role_str.replace("，", ",").split(",") if r.strip()]
            if len(roles) != 3:
                problems.append(f"角色信息不全，{func_user_req}")
                logger.error(f"角色信息不全，{func_user_req}")

            for process in item.get("功能过程", []):
                process_name = process.get("名称", "")
                sub_processes = process.get("子过程", [])
                if len(sub_processes) != 3:
                    problems.append(f"功能过程{process_name}的子过程不是三个，{func_user_req}")
                    logger.error(f"功能过程{process_name}的子过程不是三个，{func_user_req}")
        if len(problems)==0:
            logger.info("文档检查无误,可以进行下一步工作了")
        return problems

excel_utils = ExcelUtils()
if __name__ == "__main__":
    excel_utils = ExcelUtils()
    excel_utils.read_excel_to_pd()
    excel_utils.read_pd_to_json()
    excel_utils.check_info()

   
