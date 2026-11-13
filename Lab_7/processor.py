
import math


def parse_vitals_summary(vitals_csv):
    if not isinstance(vitals_csv, str):
        return "Invalid vitals input"

    parts = vitals_csv.split(',')

    if len(parts) != 3:
        return "Invalid vitals format. Expected HR,SpO2,Temp"

    try:
        hr = float(parts[0])
        spo2 = float(parts[1])
        temp = float(parts[2])

        if not all(math.isfinite(x) for x in (hr, spo2, temp)):
            return "Invalid vitals values"

    except ValueError:
        return "Invalid vitals values"

    critical = hr > 120 or spo2 < 90 or temp > 39.0

    return f"Vitals: HR={hr}, SpO2={spo2}% - {'CRITICAL' if critical else 'STABLE'}"


def compute_patient_bmi(bmi_string):
    if not isinstance(bmi_string, str):
        return "Invalid BMI input"

    parts = bmi_string.split('/')

    if len(parts) != 2:
        return "Invalid BMI format. Expected weight/height"

    try:
        weight = float(parts[0])
        height = float(parts[1])

        if not math.isfinite(weight) or not math.isfinite(height):
            return "Invalid weight or height"

        if weight <= 0 or height <= 0:
            return "Weight and height must be positive"

        bmi = weight / (height ** 2)

        if not math.isfinite(bmi):
            return "Invalid BMI calculation"

        return round(bmi, 2)

    except (ValueError, OverflowError):
        return "Invalid weight or height"


def assign_ward_bed(allocation_code):
    if not isinstance(allocation_code, str):
        return "Invalid allocation input"

    parts = allocation_code.strip().split('-')

    if len(parts) != 2:
        return "Invalid allocation format. Expected WARD-BED"

    ward, bed_str = parts

    ward_names = {
        "ER": "Emergency Room",
        "ICU": "Intensive Care Unit",
        "GEN": "General Ward",
        "PED": "Pediatrics"
    }

    try:
        bed_num = int(bed_str)

        if bed_num <= 0:
            return "Invalid bed number"

    except ValueError:
        return "Invalid bed number"

    ward = ward.upper()

    if ward not in ward_names:
        return "Invalid ward code"

    return f"{ward_names[ward]} Bed #{bed_num}"


def main():
    print("==== Running parse_vitals_summary ====")
    v_input = input("Enter vitals (HR,SpO2,Temp): ")
    print("Summary:", parse_vitals_summary(v_input))

    print("\n==== Running compute_patient_bmi ====")
    b_input = input("Enter weight/height (e.g. 70/1.75): ")
    print("BMI:", compute_patient_bmi(b_input))

    print("\n==== Running assign_ward_bed ====")
    w_input = input("Enter allocation (e.g. ICU-05): ")
    print("Assignment:", assign_ward_bed(w_input))


if __name__ == "__main__":
    main()
