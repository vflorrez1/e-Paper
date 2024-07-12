import json
from datetime import datetime


def format_number_with_decimal(num: int) -> str:
    num_str = str(num)

    if len(num_str) < 3:
        # Prepend "0." and then zeros if necessary to ensure 3 digits after the decimal
        num_str = "0." + num_str.zfill(3)
    else:
        # Insert a decimal point before the 3rd last character
        num_str = num_str[:-3] + "." + num_str[-3:]

    return num_str


def parse_racer(racer: dict) -> dict:
    racer_data = {
        "name": racer["N"],
        "driverId": racer["D"],
        "position": racer["P"],
        "lap": racer["L"],
        "currentLapTime": format_number_with_decimal(racer["T"]),
        "bestLapTime": format_number_with_decimal(racer["B"]),
        "delta": format(
            float(format_number_with_decimal(racer["T"])) -
            float(format_number_with_decimal(racer["B"])),
            ".3f"
        ),
        "gap": racer["G"],
        "kartNumber": racer["K"],
        "averageLapTime": format_number_with_decimal(racer["A"]),
    }
    return racer_data

def milliseconds_to_mm_ss(milliseconds):
    # Convert milliseconds to total seconds
    total_seconds = milliseconds / 1000
    
    # Calculate minutes and remaining seconds
    minutes, seconds = divmod(total_seconds, 60)
    
    # Format minutes and seconds as two-digit strings
    minutes_str = f"{int(minutes):02}"
    seconds_str = f"{int(seconds):02}"
    
    return f"{minutes_str}:{seconds_str}"


def parse_object(data: dict, name: str) -> None:
    data = json.loads(data)
    session_data = {
        "sessionStartTime": datetime.fromtimestamp(data["T"]).strftime('%Y-%m-%d %H:%M:%S'),
        "sessionName": data["N"],
        "sessionLaps": data["L"],
        "sessionCountDown": milliseconds_to_mm_ss(data["C"]),
    }

    racer_data = next((racer for racer in data["D"] if racer["N"] == name), None)
    
    print("Session Data:")
    print(json.dumps(session_data, indent=4))

    print("Racer Data:")
    if racer_data:
        new_ob = {
            "session": session_data,
            "racer": parse_racer(racer_data)
        }
        return new_ob
    else:
        other_ob = {
            "session": session_data,
            "racer": None
        }
        return other_ob

