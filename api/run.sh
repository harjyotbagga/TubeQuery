docker run -p 6379:6379 -d redis
uvicorn main:app --reload