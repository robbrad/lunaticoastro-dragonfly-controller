from dragonfly_dome.controller import DragonFlyDomeController
import connexion
from flask import jsonify, Flask, Response
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment Variables
DRAGONFLY_IP = os.getenv('DRAGONFLY_IP')
DRAGONFLY_PORT = int(os.getenv('DRAGONFLY_PORT', '8080'))


def handle_controller_error(e: Exception) -> Response:
    logger.error(f"An error occurred: {str(e)}")
    return jsonify({"error": str(e)}), 500


def get_sensor_data(sensor_id: int) -> Response:
    try:
        with DragonFlyDomeController(DRAGONFLY_IP, DRAGONFLY_PORT) as controller:
            status = controller.get_sensor_data(sensor_id)
            sensor_info = controller.parse_sensor_info(status)
            return jsonify({"sensor": sensor_info})
    except Exception as e:
        return handle_controller_error(e)


def get_relay_data(relay_id: int) -> Response:
    try:
        with DragonFlyDomeController(DRAGONFLY_IP, DRAGONFLY_PORT) as controller:
            status = controller.get_relay_data(relay_id)
            relay_info = controller.parse_relay_info(status)
            return jsonify({"relay": relay_info})
    except Exception as e:
        return handle_controller_error(e)


def get_all_sensor_data() -> Response:
    try:
        with DragonFlyDomeController(DRAGONFLY_IP, DRAGONFLY_PORT) as controller:
            sensors = [controller.parse_sensor_info(controller.get_sensor_data(i)) for i in range(8)]
            return jsonify({"sensors": sensors})
    except Exception as e:
        return handle_controller_error(e)


def get_all_relay_data() -> Response:
    try:
        with DragonFlyDomeController(DRAGONFLY_IP, DRAGONFLY_PORT) as controller:
            relays = [controller.parse_relay_info(controller.get_relay_data(i)) for i in range(8)]
            return jsonify({"relays": relays})
    except Exception as e:
        return handle_controller_error(e)


def get_all_data() -> Response:
    try:
        with DragonFlyDomeController(DRAGONFLY_IP, DRAGONFLY_PORT) as controller:
            sensors = [controller.parse_sensor_info(controller.get_sensor_data(i)) for i in range(8)]
            relays = [controller.parse_relay_info(controller.get_relay_data(i)) for i in range(8)]
            return jsonify({"sensors": sensors, "relays": relays})
    except Exception as e:
        return handle_controller_error(e)


def set_relay_state(relay_id: int, state: bool) -> Response:
    try:
        with DragonFlyDomeController(DRAGONFLY_IP, DRAGONFLY_PORT) as controller:
            status = controller.set_relay_state(relay_id, state)
            return jsonify({"status": status})
    except Exception as e:
        return handle_controller_error(e)


def create_app() -> Flask:
    app = connexion.App(__name__, specification_dir="./")
    app.add_api("swagger.yaml")
    return app.app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
