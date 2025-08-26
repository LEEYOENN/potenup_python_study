FROM python:3.11-slim

WORKDIR /app
# 내가 동작시킬 파일들은 이 workdir에 위치한다

COPY requirements.txt .
# requirements.txt 파일을 컨테이너의 /app 디렉토리에 복사한다

RUN pip install -r requirements.txt
# requirements.txt에 명시된 패키지들을 설치한다
RUN pip install uvicorn fastapi
# uvicorn과 fastapi를 설치한다 -- 오류방지
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126

COPY infermain.py .
# infermain.py 파일을 컨테이너의 /app 디렉토리에 복사한다

COPY model/ ./model/
# model 디렉토리를 컨테이너의 /app 디렉토리에 복사한다

COPY imgdata/ /app/imgdata/
# imgdata 디렉토리를 컨테이너의 /app 디렉토리에 복사한다

EXPOSE 8080
# 실행할 때 사용할 포트번호

CMD ["uvicorn", "infermain:app", "--host", "0.0.0.0", "--port", "8080"]
# uvicorn을 사용하여 infermain.py 파일을 실행한다


