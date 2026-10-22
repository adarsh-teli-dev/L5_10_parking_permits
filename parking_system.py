
"""Manage campus parking permits and zone inspections."""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

PERMITS: dict[str, dict[str, str]] = {}
ZONES = {"A", "B", "C"}
DEFAULT_DATABASE = Path("permits.json")


def register_permit(
    vehicle_plate: str,
    zone_id: str,
    zone_records: list[tuple[str, str]] | None = None,
) -> str | None:
    """Register a valid vehicle for a parking zone."""
    if not isinstance(vehicle_plate, str) or not vehicle_plate.strip():
        print("Error: vehicle plate cannot be empty.")
        return None

    if not isinstance(zone_id, str) or zone_id not in ZONES:
        print(f"Error: invalid zone. Choose from {sorted(ZONES)}.")
        return None

    if zone_records is None:
        zone_records = []

    permit_number = f"P{random.randint(10000, 99999)}"
    expiry_date = datetime.now() + timedelta(days=180)

    PERMITS[vehicle_plate] = {
        "zone": zone_id,
        "permit": permit_number,
        "expiry": expiry_date.strftime("%Y-%m-%d"),
    }
    zone_records.append((vehicle_plate, zone_id))

    return permit_number


def revoke_permit(vehicle_plate: str) -> bool:
    """Revoke a permit if it exists."""
    return PERMITS.pop(vehicle_plate, None) is not None


def is_expired(vehicle_plate: str) -> bool:
    """Check whether a permit has expired."""
    permit = PERMITS.get(vehicle_plate)

    if permit is None:
        return True

    try:
        expiry_date = datetime.strptime(
            permit["expiry"], "%Y-%m-%d"
        ).date()
    except (KeyError, ValueError):
        print(f"Error: invalid expiry date for {vehicle_plate}.")
        return True

    return expiry_date < datetime.now().date()


def scan_zone(zone_id: str, plates_seen: list[str]) -> list[str]:
    """Return vehicles that should not be parked in the given zone."""
    if zone_id not in ZONES:
        raise ValueError(f"Invalid zone: {zone_id}")

    flagged_plates = []

    for plate in plates_seen:
        permit = PERMITS.get(plate)

        if (
            permit is None
            or permit["zone"] != zone_id
            or is_expired(plate)
        ):
            flagged_plates.append(plate)

    return flagged_plates


def load_permit_database(
    file: str | Path = DEFAULT_DATABASE,
) -> bool:
    """Load permits from a JSON database."""
    global PERMITS

    try:
        with open(file, "r", encoding="utf-8") as permit_file:
            loaded_permits: Any = json.load(permit_file)
    except FileNotFoundError:
        PERMITS = {}
        return True
    except (OSError, json.JSONDecodeError) as error:
        print(f"Error loading permit database: {error}")
        return False

    if not isinstance(loaded_permits, dict):
        print("Error: permit database must contain a JSON object.")
        return False

    PERMITS = loaded_permits
    return True


def save_permit_database(
    file: str | Path = DEFAULT_DATABASE,
) -> bool:
    """Save permits to a JSON database."""
    try:
        with open(file, "w", encoding="utf-8") as permit_file:
            json.dump(PERMITS, permit_file, indent=4)
    except OSError as error:
        print(f"Error saving permit database: {error}")
        return False

    return True


def set_expiry(vehicle_plate: str, date_text: str) -> bool:
    """Set a permit expiry date using YYYY-MM-DD."""
    permit = PERMITS.get(vehicle_plate)

    if permit is None:
        print(f"Error: no permit found for {vehicle_plate}.")
        return False

    try:
        expiry_date = datetime.strptime(date_text, "%Y-%m-%d").date()
    except ValueError:
        print("Error: date must use YYYY-MM-DD format.")
        return False

    permit["expiry"] = expiry_date.isoformat()
    return True


def main() -> None:
    """Run a demonstration of the parking permit manager."""
    if not load_permit_database():
        print("Continuing with the in-memory permit data.")

    register_permit("KA01AB1234", "A")
    register_permit("KA05XY9999", "Z")  # Intentionally invalid test.
    register_permit("", "B")  # Intentionally invalid test.

    set_expiry("KA01AB1234", "2020-01-01")

    revoke_permit("MH12ZZ0000")

    print(
        "Flagged in zone A:",
        scan_zone(
            "A",
            ["KA01AB1234", "KA05XY9999", "TN09QQ1111"],
        ),
    )

    plate = input("Plate to revoke (Enter to skip): ").strip()
    if plate and not revoke_permit(plate):
        print(f"No permit found for {plate}.")

    if save_permit_database():
        print("Permit database saved successfully.")

    print("Permits on file:", len(PERMITS))


if __name__ == "__main__":
    main()
