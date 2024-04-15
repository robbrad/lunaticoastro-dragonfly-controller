import socket
import re
from typing import Optional, Tuple, Dict


class DragonFlyDomeController:
    OPERATIVES = ["", "Bootloader", "Error"]
    MODELS = ["Error", "Seletek", "Armadillo", "Platypus", "Dragonfly"]

    def __init__(self, ip: str, port: int) -> None:
        """
        Initializes the controller with IP and port.

        Parameters:
            ip (str): The IP address of the dome controller.
            port (int): The port number on which the dome controller is listening.
        """
        self.ip: str = ip
        self.port: int = port
        self.sock: Optional[socket.socket] = None

    def __enter__(self) -> "DragonFlyDomeController":
        """
        Context manager entry handling. Opens the socket.

        Returns:
            self (DragonFlyDomeController): The instance itself.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(2)
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_value: Optional[Exception],
        traceback: Optional[type],
    ) -> None:
        """
        Context manager exit handling. Closes the socket.

        Parameters:
            exc_type (Optional[type]): The exception type if raised.
            exc_value (Optional[Exception]): The exception instance if raised.
            traceback (Optional[type]): The traceback if an exception was raised.
        """
        if self.sock:
            self.sock.close()

    def send_command(self, command: str) -> str:
        """
        Sends a command to the dome controller and retrieves the response.

        Parameters:
            command (str): The command string to be sent.

        Returns:
            response (str): The response from the dome controller.
        """
        if self.sock is None:
            raise RuntimeError("Connection not established.")

        for attempt in range(3):
            try:
                self.sock.sendto(command.encode(), (self.ip, self.port))
                data, _ = self.sock.recvfrom(1024)
                return data.decode().strip()
            except socket.timeout:
                if attempt == 2:  # Last attempt
                    raise TimeoutError(
                        f"Command '{command}' timed out after 3 attempts"
                    )
            except socket.error as e:
                raise ConnectionError(
                    f"Socket error during command '{command}': {str(e)}"
                )

    def get_relay_status(self, relay_id: int) -> str:
        """
        Retrieves the status of a specified relay.

        Parameters:
            relay_id (int): The ID of the relay to query.

        Returns:
            status (str): 'closed' if the relay is closed, 'open' otherwise.
        """
        command = f"!relio rldgrd 0 {relay_id}#"
        response = self.send_command(command)
        return "closed" if response and response.endswith("1#") else "open"

    def get_sensor_status(self, sensor_id: int) -> str:
        """
        Retrieves the status of a specified sensor.

        Parameters:
            sensor_id (int): The ID of the sensor to query.

        Returns:
            status (str): The status of the sensor, or 'unknown' if not determinable.
        """
        command = f"!relio snanrd 0 {sensor_id}#"
        response = self.send_command(command)
        return response.split(":")[1].strip("#") if response else "unknown"

    def get_relay_data(self, relay_id: int) -> str:
        """
        Retrieves the data and status for a specific relay.

        Parameters:
            relay_id (int): The ID of the relay to query.

        Returns:
            relay_data (str): A string containing both the data and the status of the relay.
        """
        relay_data = self.send_command(f"!relio getreldata {relay_id}#")
        status = self.get_relay_status(relay_id)
        relay = relay_data + "," + status
        return relay

    def get_sensor_data(self, sensor_id: int) -> str:
        """
        Retrieves the data and status for a specific sensor.

        Parameters:
            sensor_id (int): The ID of the sensor to query.

        Returns:
            sensor_data (str): A string containing both the data and the status of the sensor.
        """
        sensor_data = self.send_command(f"!relio getsendata {sensor_id}#")
        status = self.get_sensor_status(sensor_id)
        sensor = sensor_data + "," + status
        return sensor

    @staticmethod
    def parse_relay_info(relay_string: str) -> Dict[str, any]:
        """
        Parses relay information from a string.

        Parameters:
            relay_string (str): The string containing relay data.

        Returns:
            relay_info (Dict[str, any]): A dictionary containing relay details such as name, activity status, and state.
        """
        parts = relay_string.split(",")
        is_active = parts[3].isdigit() and parts[3] == "1"
        relay_info = {
            "name": parts[0].split(":")[-1],
            "is_active": is_active,
            "state": parts[-1],
        }
        return relay_info

    @staticmethod
    def parse_sensor_info(sensor_string: str) -> Dict[str, any]:
        """
        Parses sensor information from a string.

        Parameters:
            sensor_string (str): The string containing sensor data.

        Returns:
            sensor_info (Dict[str, any]): A dictionary containing sensor details such as name and value.
        """
        parts = sensor_string.split(",")
        sensor_info = {"name": parts[0].split(":")[-1], "value": parts[-1]}
        return sensor_info

    @staticmethod
    def parse_version_response(response: str) -> int:
        """
        Parses the version response from the controller.

        Parameters:
            response (str): The response string containing version data.

        Returns:
            version (int): The numeric version extracted from the response.
        """
        match = re.search(r"(\d+)", response)
        if match:
            return int(match.group(1))
        else:
            raise ValueError("No numeric version info found in response.")

    def change_relay_state(self, relay_id: int) -> str:
        """
        Changes the state of the specified relay.

        Parameters:
            relay_id (int): The ID of the relay whose state is to be toggled.

        Returns:
            response (str): The response from the controller after the command execution.
        """
        command = f"!relio rlchg 2 {relay_id} 1#"
        response = self.send_command(command)
        return response

    def set_relay_state(self, relay_id: int, state: str) -> str:
        """
        Sets the state of the specified relay.

        Parameters:
            relay_id (int): The ID of the relay whose state is to be set.
            state (str): The desired state ('closed' or 'open').

        Returns:
            response (str): The response from the controller after the command execution.
        """
        state_val = "1" if state == "closed" else "0"
        command = f"!relio rlset 2 {relay_id} {state_val}#"
        response = self.send_command(command)
        return response

    def echo(self) -> Optional[str]:
        """
        Sends a version query to the controller and processes the response.

        Returns:
            version_info (Optional[str]): A string describing the version or None if an error occurred.
        """
        response = self.send_command("!seletek version#")
        if response:
            try:
                res = self.parse_version_response(response.strip())
            except ValueError as e:
                print(e)
                return None

            oper = res // 10000  # Operational mode
            model = (res // 1000) % 10  # Model
            fwmaj = (res // 100) % 10  # Firmware major version
            fwmin = res % 100  # Firmware minor version

            if oper >= len(self.OPERATIVES):
                oper = -1
            if model >= len(self.MODELS):
                model = 0

            version_info = (
                f"{self.OPERATIVES[oper]} {self.MODELS[model]} fwv {fwmaj}.{fwmin}"
            )
            if self.MODELS[model] != "Dragonfly":
                print(
                    f"Warning: Detected model is {self.MODELS[model]} while Dragonfly model is expected."
                )
            print(f"Setting version to [{version_info}]")
            return version_info
        else:
            print("Failed to receive firmware version.")
            return None
