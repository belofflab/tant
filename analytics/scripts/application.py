import uvicorn


def start_fastapi():
  uvicorn.run(
    'src.application:app',
    host='0.0.0.0', port=9900, reload=True
  )