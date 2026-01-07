import csv

total_risk = 0
max_risk = 0
failed_controls = []

print("=== Security Risk Assessment Tool ===\n")

with open("controls.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        control = row["Control"]
        likelihood = int(row["Likelihood"])
        impact = int(row["Impact"])

        answer = input(f"Is '{control}' implemented? (yes/no): ").lower()

        risk_value = likelihood * impact
        max_risk += risk_value

        if answer != "yes":
            total_risk += risk_value
            failed_controls.append((control, risk_value, row["ISO27001"], row["NIST"]))


risk_percentage = (total_risk / max_risk) * 100

# Risk Level
if risk_percentage < 30:
    risk_level = "LOW"
elif risk_percentage < 60:
    risk_level = "MEDIUM"
else:
    risk_level = "HIGH"

print("\n=== Assessment Result ===")
print(f"Overall Risk Score: {risk_percentage:.2f}%")
print(f"Risk Level: {risk_level}")


print("\nFailed Controls (Compliance Mapping):")
for control, value, iso, nist in failed_controls:
    print(f"- {control} | Risk: {value}")
    print(f"  ISO 27001: {iso}")
    print(f"  NIST: {nist}")


print("\nRecommendations:")
if not failed_controls:
    print("- All critical security controls are in place.")
else:
    for control, _ in failed_controls:
        if "Password" in control:
            print("- Enforce strong password policies.")
        elif "Backup" in control:
            print("- Implement regular and secure backups.")
        elif "Antivirus" in control:
            print("- Install and maintain antivirus software.")
        elif "Firewall" in control:
            print("- Enable and configure firewall rules.")
        elif "OS" in control:
            print("- Keep the operating system updated.")

# Report Generation

with open("risk_report.txt", "w") as report:
    report.write("Security Risk Assessment Report\n")
    report.write("===============================\n\n")
    report.write(f"Overall Risk Score: {risk_percentage:.2f}%\n")
    report.write(f"Risk Level: {risk_level}\n\n")

    if failed_controls:
        report.write("Risk Findings:\n")
        for control, value, iso, nist in failed_controls:
            report.write(f"- {control}\n")
            report.write(f"  Risk Value: {value}\n")
            report.write(f"  ISO 27001: {iso}\n")
            report.write(f"  NIST: {nist}\n\n")
    else:
        report.write("No significant risks identified.\n")
