from os import getenv

import uvicorn

port = getenv("PORT", 8000)

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=port, reload=True, debug=True)
