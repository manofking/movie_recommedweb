# 1.  파이썬 3.13 버전 사용
FROM python:3.13-slim

# 2. 작업 디렉토리를 /app으로  지정
WORKDIR /app

# 3. 
EXPOSE 80


# 4. OpenMP 라이브러리(libgomp1) 
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 5. requirements.txt 복사 및 패키지 설치
COPY requirements.txt .


# 6. 패키지 설치 
RUN python3 -m pip install --no-cache-dir --upgrade \
    setuptools \
    wheel \
    && \
    python3 -m pip install --trusted-host pypi.python.org -r requirements.txt

# 7. 
COPY ./App .

# 8. 실행 명령
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]








