from src.payroll_service import parse_payroll

payroll = "09926/0400"
service = None

result = parse_payroll(payroll, service)

print(result)