from dragonfly_dome.controller import DragonFlyDomeController
import connexion
from flask import jsonify
import os

DRAGONFLY_IP = os.getenv('DRAGONFLY_IP')
DRAGONFLY_PORT = int(os.getenv('DRAGONFLY_PORT'))


def get_sensor_data(sensor_id):
    try:
        with DragonFlyDomeController(DRAGONFLY_IP, DRAGONFLY_PORT) as controller:
            status = controller.get_sensor_data(sensor_id)
            return jsonify({"sensor": [controller.parse_sensor_info(status)]})
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def get_relay_data(relay_id):
    try:
        with DragonFlyDomeController(DRAGONFLY_IP, DRAGONFLY_PORT) as controller:
            status = controller.get_relay_data(relay_id)
            return jsonify({"relay": [controller.parse_relay_info(status)]})
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def get_all_relay_data():
    try:
        with DragonFlyDomeController(DRAGONFLY_IP, DRAGONFLY_PORT) as controller:
            relays = []
            for i in range(8):
                status = controller.get_relay_data(i)
                relay_info = controller.parse_relay_info(status)
                # Directly append the dictionary, assuming parse_relay_info returns a dict
                relays.append(relay_info)
            # No need to load JSON here, just prepare the final dictionary
            relays_json = {"relays": relays}
            # Return a JSON string
            return jsonify(relays_json)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # It's good practice to return None or raise the exception again after logging it
        return None


def get_all_data():
    try:
        with DragonFlyDomeController(DRAGONFLY_IP, DRAGONFLY_PORT) as controller:
            sensors = []
            relays = []
            for i in range(8):
                sensor_status = controller.get_sensor_data(i)
                # Assuming parse_sensor_info returns a JSON string
                sensor_info = controller.parse_sensor_info(sensor_status)
                sensors.append(sensor_info)
                relay_status = controller.get_relay_data(i)
                relay_info = controller.parse_relay_info(relay_status)
                relays.append(relay_info)
            # Now, create a dictionary that wraps the list of sensor data
            data_dict = {"sensors": sensors, "relays": relays}
            # If you need to return a JSON string instead of a dictionary
            return jsonify(data_dict)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {}  # Return an empty dictionary in case of an error

def get_all_sensor_data():
    try:
        with DragonFlyDomeController(DRAGONFLY_IP, DRAGONFLY_PORT) as controller:
            sensors = []
            for i in range(8):
                status = controller.get_sensor_data(i)
                # Assuming parse_sensor_info returns a JSON string
                sensor_info = controller.parse_sensor_info(status)
                sensors.append(sensor_info)
            # Now, create a dictionary that wraps the list of sensor data
            sensors_dict = {"sensors": sensors}
            # If you need to return a JSON string instead of a dictionary
            return jsonify(sensors_dict)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {}  # Return an empty dictionary in case of an error


def set_relay_state(relay_id, state):
    try:
        with DragonFlyDomeController(DRAGONFLY_IP, DRAGONFLY_PORT) as controller:
            status = controller.set_relay_state(relay_id, state)
            return status
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def create_app():
    app = connexion.App(__name__, specification_dir="./")
    app.add_api("swagger.yaml")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
