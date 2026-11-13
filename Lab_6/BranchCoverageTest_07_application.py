
import pytest
from hospital_triage_priority import (
    process_triage_wards,
    monitor_oxygen_manifolds
)


# 1. Input validation branches

def test_invalid_wards_type():
    with pytest.raises(ValueError):
        process_triage_wards(None, 10)


def test_negative_acuity_score():
    with pytest.raises(ValueError):
        process_triage_wards([], -1)


def test_valid_empty_wards():
    result = process_triage_wards([], 10)
    assert result["status"] == "NO_URGENT_CASES"


# 2. Ward acceptance and patient iteration branches

def test_non_accepting_ward():
    result = process_triage_wards(
        [{"is_accepting": False}], 10
    )
    assert result["status"] == "NO_URGENT_CASES"


def test_accepting_ward_without_patients():
    result = process_triage_wards(
        [{"is_accepting": True}], 10
    )
    assert result["status"] == "NO_URGENT_CASES"


# 3. Invalid vital signs branches

def test_invalid_spo2():
    wards = [{
        "is_accepting": True,
        "patients": [{"spo2": 0, "hr": 75}]
    }]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0


def test_invalid_heart_rate():
    wards = [{
        "is_accepting": True,
        "patients": [{"spo2": 98, "hr": 0}]
    }]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0


# 4. Consciousness branches

def test_unconscious_general_patient():
    wards = [{
        "is_accepting": True,
        "tier": "general",
        "patients": [{"unconscious": True}]
    }]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 100


def test_unconscious_outpatient():
    wards = [{
        "is_accepting": True,
        "tier": "outpatient",
        "patients": [
            {"unconscious": True},
            {"unconscious": False}
        ]
    }]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0


def test_conscious_normal_patient():
    wards = [{
        "is_accepting": True,
        "patients": [{"unconscious": False}]
    }]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 10


# 5. Critical vital sign branches

def test_low_spo2():
    wards = [{
        "is_accepting": True,
        "patients": [{"spo2": 89, "hr": 75}]
    }]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 60


def test_high_heart_rate():
    wards = [{
        "is_accepting": True,
        "patients": [{"spo2": 98, "hr": 121}]
    }]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 60


def test_normal_threshold_values():
    wards = [{
        "is_accepting": True,
        "patients": [{"spo2": 90, "hr": 120}]
    }]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 10


# 6. ICU standby branches

def test_icu_standby_enabled():
    wards = [{
        "is_accepting": True,
        "icu_standby": True,
        "patients": [{"spo2": 98, "hr": 75}]
    }]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 35


def test_icu_standby_disabled():
    wards = [{
        "is_accepting": True,
        "icu_standby": False,
        "patients": [{"spo2": 98, "hr": 75}]
    }]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 10


# 7. Flagged entries threshold branches

def test_exactly_four_flagged_entries():
    wards = [{
        "is_accepting": True,
        "patients": [{"spo2": 0, "hr": 75}] * 4
    }]
    result = process_triage_wards(wards, 10)
    assert result["status"] == "NO_URGENT_CASES"


def test_more_than_four_flagged_entries():
    wards = [{
        "is_accepting": True,
        "patients": [{"spo2": 0, "hr": 75}] * 5
    }]
    result = process_triage_wards(wards, 10)
    assert result["status"] == "WARD_ALERT"


# 8. Multiple wards and patients

def test_multiple_wards():
    wards = [
        {
            "is_accepting": True,
            "patients": [{"spo2": 98, "hr": 75}]
        },
        {
            "is_accepting": False,
            "patients": [{"spo2": 80, "hr": 130}]
        },
        {
            "is_accepting": True,
            "icu_standby": True,
            "patients": [{"spo2": 89, "hr": 75}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 95
    assert result["status"] == "TRIAGE_STABLE"


# 9. Oxygen manifold branches

def test_no_sensor_data():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_pressure_failure():
    assert monitor_oxygen_manifolds(
        [[5.0, 3.5, 3.0]]
    ) == "PRESSURE_FAILURE"


def test_single_pressure_drop():
    assert monitor_oxygen_manifolds(
        [[5.0, 3.5, 5.0]]
    ) == "PRESSURE_NORMAL"


def test_pressure_recovery_resets_streak():
    assert monitor_oxygen_manifolds(
        [[3.5, 5.0, 3.5, 5.0]]
    ) == "PRESSURE_NORMAL"


def test_empty_manifold():
    assert monitor_oxygen_manifolds(
        [[]]
    ) == "PRESSURE_NORMAL"


def test_multiple_manifolds():
    assert monitor_oxygen_manifolds(
        [[], [5.0, 4.5, 3.5, 3.0]]
    ) == "PRESSURE_FAILURE"
