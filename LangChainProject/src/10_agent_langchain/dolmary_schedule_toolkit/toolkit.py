from typing import List, Dict
from langchain_core.tools import BaseTool
from langchain.agents.agent_toolkits.base import BaseToolkit

# 여기에 만들 툴들을 등록 (toolkit == tool들의 모음)

# 새로운 도구 추가
from .tools import AddToDoTool, ViewToDoTool, DeleteToDoTool, SuccessedToDoTool

class DolmaryScheduleToolkit(BaseToolkit):
    """ 
    돌마리 운동회 스케줄 관리를 위한 툴킷입니다."""

    def get_tools(self) -> List[BaseTool]:
        return [AddToDoTool(), ViewToDoTool(), DeleteToDoTool(), SuccessedToDoTool()]