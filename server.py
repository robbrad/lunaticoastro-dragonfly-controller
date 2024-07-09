from fastapi import FastAPI, HTTPException
from dragonfly_dome.controller import DragonFlyDomeController
import os
import logging
from enum import Enum

app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment Variables
DRAGONFLY_IP = os.getenv('DRAGONFLY_IP', '127.0.0.1')
DRAGONFLY_PORT = int(os.getenv('DRAGONFLY_PORT', '10000'))

class Status(str, Enum):
    OPEN = 'open'
    CLOSED = 'closed'

def handle_controller_error(e: Exception):
    logger.error(f"An error occurred: {str(e)}")
    raise HTTPException(status_code=500, detail=str(e))

@app.get("/sensor/{sensor_id}")
def get_sensor_data(sensor_id: int):
    try:
        with DragonFlyDomeController(DRAGONFLY_IP, DRAGONFLY_PORT) as controller:
            status = controller.get_sensor_data(sensor_id)
            sensor_info = controller.parse_sensor_info(status)
            return {"sensor": sensor_info}
    except Exception as e:
        return handle_controller_error(e)

@app.get("/relay/{relay_id}")
def get_relay_data(relay_id: int):
    try:
        with DragonFlyDomeController(DRAGONFLY_IP, DRAGONFLY_PORT) as controller:
            status = controller.get_relay_data(relay_id)
            relay_info = controller.parse_relay_info(status)
            return {"relay": relay_info}
    except Exception as e:
        return handle_controller_error(e)

@app.get("/sensors")
def get_all_sensor_data():
    try:
        with DragonFlyDomeController(DRAGONFLY_IP, DRAGONFLY_PORT) as controller:
            sensors = [controller.parse_sensor_info(controller.get_sensor_data(i)) for i in range(8)]
            return {"sensors": sensors}
    except Exception as e:
        return handle_controller_error(e)

@app.get("/relays")
def get_all_relay_data():
    try:
        with DragonFlyDomeController(DRAGONFLY_IP, DRAGONFLY_PORT) as controller:
            relays = [controller.parse_relay_info(controller.get_relay_data(i)) for i in range(8)]
            return {"relays": relays}
    except Exception as e:
        return handle_controller_error(e)

@app.get("/all")
def get_all_data():
    try:
        with DragonFlyDomeController(DRAGONFLY_IP, DRAGONFLY_PORT) as controller:
            sensors = [controller.parse_sensor_info(controller.get_sensor_data(i)) for i in range(8)]
            relays = [controller.parse_relay_info(controller.get_relay_data(i)) for i in range(8)]
            return {"sensors": sensors, "relays": relays}
    except Exception as e:
        return handle_controller_error(e)

@app.put("/relay/{relay_id}")
def set_relay_state(relay_id: int, state: Status):
    try:
        with DragonFlyDomeController(DRAGONFLY_IP, DRAGONFLY_PORT) as controller:
            status = controller.set_relay_state(relay_id, state)
            return {"status": status}
    except Exception as e:
        return handle_controller_error(e)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
