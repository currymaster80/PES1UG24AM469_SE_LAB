
import pytest
from hospital_triage_priority import (
    process_triage_wards,
    monitor_oxygen_manifolds
)


def test_invalid_wards_type():
    with pytest.raises(ValueError):
        process_triage_wards(None, 10)


def test_negative_default_acuity():
    with pytest.raises(ValueError):
        process_triage_wards([], -1)


def test_non_accepting_ward():
    wards = [{"is_accepting": False}]
    result = process_triage_wards(wards, 10)
    assert result == {
        "acuity_score": 0,
        "status": "NO_URGENT_CASES"
    }


def test_patient_default_values():
    wards = [
        {
            "is_accepting": True,
            "patients": [{}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 10
    assert result["status"] == "TRIAGE_STABLE"


def test_invalid_spo2():
    wards = [
        {
            "is_accepting": True,
            "patients": [{"spo2": 0, "hr": 75}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0


def test_invalid_heart_rate():
    wards = [
        {
            "is_accepting": True,
            "patients": [{"spo2": 98, "hr": 0}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0


def test_unconscious_general_patient():
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "patients": [{"spo2": 98, "hr": 75, "unconscious": True}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 100


def test_unconscious_outpatient():
    wards = [
        {
            "is_accepting": True,
            "tier": "outpatient",
            "icu_standby": True,
            "patients": [
                {"spo2": 98, "hr": 75, "unconscious": False},
                {"spo2": 98, "hr": 75, "unconscious": True},
                {"spo2": 98, "hr": 75, "unconscious": False}
            ]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 25


def test_low_spo2_patient():
    wards = [
        {
            "is_accepting": True,
            "patients": [{"spo2": 89, "hr": 75}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 60


def test_high_heart_rate_patient():
    wards = [
        {
            "is_accepting": True,
            "patients": [{"spo2": 98, "hr": 121}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 60


def test_icu_standby():
    wards = [
        {
            "is_accepting": True,
            "icu_standby": True,
            "patients": [{"spo2": 98, "hr": 75}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 35


def test_ward_alert():
    wards = [
        {
            "is_accepting": True,
            "patients": [
                {"spo2": 0, "hr": 75},
                {"spo2": 0, "hr": 75},
                {"spo2": 0, "hr": 75},
                {"spo2": 0, "hr": 75},
                {"spo2": 0, "hr": 75}
            ]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["status"] == "WARD_ALERT"


def test_empty_sensor_streams():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_pressure_failure():
    streams = [[5.0, 3.5, 3.0]]
    assert monitor_oxygen_manifolds(streams) == "PRESSURE_FAILURE"


def test_pressure_normal():
    streams = [[5.0, 3.5, 4.5, 3.8, 5.0]]
    assert monitor_oxygen_manifolds(streams) == "PRESSURE_NORMAL"
