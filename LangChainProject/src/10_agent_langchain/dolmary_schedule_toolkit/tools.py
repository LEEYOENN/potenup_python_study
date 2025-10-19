from typing import List, Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

# 스케줄 등록하는 리스트
# 1. 스케줄 등록
# 2. 스케줄 확인 도구
dol_schedule: List[str] = []

# dto 스키마 정의
# 1-1. 스케줄 스키마 설정
class AddToDoInput(BaseModel):
    time: str = Field(description="오늘 할 돌마리 스케줄 시간")
    schedule: str = Field(description="오늘 할 돌마리 스케줄 항목")
    successed: bool = Field(default=False, description="스케줄 완료 여부")

# 1-2. 스케줄 등록 도구 설정
class AddToDoTool(BaseTool):
    name: str = "add_todo"
    description: str = "돌마리 스케줄에 시간과 일정을 나누어 새 항목을 추가합니다."
    args_schema: Type[BaseModel] = AddToDoInput

    def _run(self, time: str, schedule: str) -> str:
        dol_schedule.append({"time": time, "schedule": schedule, "successed": False})
        return f"{time}에 {schedule}이 돌마리 스케줄에 등록되었습니다."

# 2-1. 스케줄 확인 스키마

# 2-2. 스케줄 확인 도구 설정
class ViewToDoTool(BaseTool):
    name: str = "view_todos"
    description: str = "현재 돌마리 스케줄 전체 목록을 보여줍니다."

    def _run(self) -> str:
        if not dol_schedule:
            return "등록된 스케줄이 없습니다."
        result = ""
        for schedule in dol_schedule:
            temp = f"시간: {schedule['time']}, 일정: {schedule['schedule']}\n"
            result += temp
        #all_schedule = "\n".join(dol_schedule)
        return f"등록된 스케줄 목록: \n{result}"
    

# 3-1 스케줄 삭제 스키마
class DeleteToDoInput(BaseModel):
    time: str = Field(description="삭제할 오늘 돌마리 스케줄 시간")
    schedule: str = Field(description="삭제할 오늘 돌마리 스케줄 항목")

# 3-2 스케줄 삭제 도구 설정
class DeleteToDoTool(BaseTool):
    name: str = "delete_todo"
    description: str = "돌마리 스케줄에서 시간이 일치하거나, 항목이 일치하는 일정을 삭제합니다."
    args_schema: Type[BaseModel] = DeleteToDoInput

    def _run(self, time: str, schedule: str) -> str:
        for i, item in enumerate(dol_schedule):
            # print("삭제 시도:", time, schedule)
            # print("현재 스케줄:", dol_schedule)
            if item["time"].strip() == time.strip() or item["schedule"].strip() == schedule.strip():
                del dol_schedule[i]
                return f"{time}에 {schedule} 일정이 삭제되었습니다."
        return f"{time}에 {schedule} 일정이 없습니다."
    
# 4-1 스케줄 완료 확인 스키마
class SuccessedToDoInput(BaseModel):
    time: str = Field(description="완료 확인할 오늘 돌마리 스케줄")
    schedule: str = Field(description="완료 확인할 오늘 돌마리 스케줄 항목")

# 4-2 스케줄 완료 확인 도구 설정
class SuccessedToDoTool(BaseTool):
    name: str = "successed_todo"
    description: str = "돌마리 스케줄에서 시간이 일치하거나 항목이 일치하는 일정을 완료로 전환하고 결과를 확인합니다."
    args_schema: Type[BaseModel] = SuccessedToDoInput

    def _run(self, time: str, schedule: str) -> str:
        for i, item in enumerate(dol_schedule):
            if item["time"].strip() == time.strip() or item["schedule"].strip() == schedule.strip():
                dol_schedule[i]["successed"] = True
                print(f"{time}에 {schedule} 일정이 성공적으로 완료되었습니다.")

        for i, item in enumerate(dol_schedule):
            if item["time"].strip() == time.strip() or item["schedule"].strip() == schedule.strip():
                if dol_schedule[i]["successed"] == True:
                    return f"{time}에 {schedule} 일정이 성공적으로 완료되었습니다."
                else: 
                    return f"{time}에 {schedule} 일정이 완료 등록되지 않았습니다."
        return f"{time}에 {schedule} 일정이 없습니다."

     


