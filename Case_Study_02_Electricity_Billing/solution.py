"""Calculate monthly electricity bills and compare usage."""

def calculate_slab_energy_charge(units):
    """Calculate energy charges using progressive tariff slabs."""
    if units <= 0:
        return 0.0
    
    charge = 0.0
    # Slab 1: 0 - 100 units @ 2.50
    if units <= 100:
        charge = units * 2.50
    # Slab 2: 101 - 200 units @ 3.75
    elif units <= 200:
        charge = (100 * 2.50) + ((units - 100) * 3.75)
    # Slab 3: 201 - 400 units @ 5.20
    elif units <= 400:
        charge = (100 * 2.50) + (100 * 3.75) + ((units - 200) * 5.20)
    # Slab 4: Above 400 units @ 7.00
    else:
        charge = (100 * 2.50) + (100 * 3.75) + (200 * 5.20) + ((units - 400) * 7.00)
    
    return round(charge, 2)


def process_monthly_billing(month_records):
    """
    Process multi-month electricity consumption records.
    month_records is a list of tuples: (month_name, units_consumed)
    Returns a list of tuples with computed billing & anomaly alerts.
    """
    fixed_meter_charge = 75.00
    surcharge_threshold = 1500.00
    surcharge_rate = 0.05       # 5% if bill exceeds threshold
    rebate_threshold = 150.00   # units
    rebate_rate = 0.03          # 3% green rebate
    spike_threshold_pct = 30.0  # 30% jump compared to previous month

    detailed_bills = []
    
    for i in range(len(month_records)):
        month_name, units = month_records[i]
        
        # Energy charge based on progressive slabs
        energy_charge = calculate_slab_energy_charge(units)
        subtotal = energy_charge + fixed_meter_charge
        
        # Surcharge calculation
        surcharge = 0.0
        if subtotal > surcharge_threshold:
            surcharge = round(subtotal * surcharge_rate, 2)
            
        # Rebate calculation
        rebate = 0.0
        if units <= rebate_threshold:
            rebate = round((subtotal + surcharge) * rebate_rate, 2)
            
        net_payable = round(subtotal + surcharge - rebate, 2)
        
        # Anomaly detection against previous month
        anomaly_flag = "NORMAL"
        pct_change = 0.0
        if i > 0:
            prev_month, prev_units = month_records[i - 1]
            if prev_units > 0:
                pct_change = round(((units - prev_units) / prev_units) * 100, 2)
                if pct_change >= spike_threshold_pct:
                    anomaly_flag = f"SPIKE (+{pct_change}%)"
                elif pct_change <= -30.0:
                    anomaly_flag = f"DROP ({pct_change}%)"
            elif units > 0:
                anomaly_flag = "NEW CONSUMPTION"
        
        # Store detailed bill as tuple
        bill_entry = (
            month_name,
            units,
            energy_charge,
            fixed_meter_charge,
            surcharge,
            rebate,
            net_payable,
            anomaly_flag
        )
        detailed_bills.append(bill_entry)
        
    return detailed_bills


def display_billing_statement(consumer_info, bills):
    """Print an itemized and formatted monthly billing report."""
    consumer_id, consumer_name, meter_no = consumer_info
    
    separator = "=" * 88
    dash_line = "-" * 88
    
    print("\n" + separator)
    print(" " * 24 + "DR. RVR NRI POWER DISTRIBUTION CORP.")
    print(" " * 22 + "PROGRESSIVE ELECTRICITY BILLING STATEMENT")
    print(separator)
    print(f"Consumer ID : {consumer_id:<15} Consumer Name : {consumer_name}")
    print(f"Meter Number: {meter_no:<15} Tariff Class  : Domestic (LT-1)")
    print(dash_line)
    
    # Table Header
    print(f"{'Month':<10}{'Units':>7}{'Energy(Rs)':>12}{'Fixed(Rs)':>11}{'Surch(Rs)':>11}{'Rebate(Rs)':>12}{'Net Pay(Rs)':>13}{'Status':>12}")
    print(dash_line)
    
    total_units = 0
    total_billed = 0.0
    anomalies = []
    
    # Iterate and unpack each bill tuple
    for entry in bills:
        month, units, energy, fixed, surch, reb, net, status = entry
        total_units += units
        total_billed += net
        
        if "SPIKE" in status:
            anomalies.append((month, units, status))
            
        print(f"{month:<10}{units:>7.1f}{energy:>12.2f}{fixed:>11.2f}{surch:>11.2f}{reb:>12.2f}{net:>13.2f}  {status:<12}")
        
    print(dash_line)
    avg_units = round(total_units / len(bills), 2) if len(bills) > 0 else 0
    avg_bill = round(total_billed / len(bills), 2) if len(bills) > 0 else 0
    print(f"Total Consumption : {total_units:.1f} Units  | Average Monthly Consumption : {avg_units:.1f} Units")
    print(f"Total Cumulative  : Rs {total_billed:,.2f} | Average Monthly Billed Amt  : Rs {avg_bill:,.2f}")
    print(dash_line)
    
    if len(anomalies) > 0:
        print("[!] ANOMALY AUDIT REPORT:")
        for anom in anomalies:
            m, u, s = anom
            print(f"    - Month {m}: {u} units recorded -> Unusual surge detected: {s}")
        print("    Recommendation: Inspect meter wiring or audit high-power appliances for faults.")
    else:
        print("[*] Consumption profile is stable across all recorded billing cycles.")
    print(separator + "\n")


def run_demo():
    """Automated demonstration with verified test dataset."""
    consumer = ("CONS-50921", "Sri Durga Prasad", "MTR-AP-8841")
    
    # 6-Month consumption dataset demonstrating slabs, surcharges, rebates, and spikes
    monthly_data = [
        ("January", 90.0),    # Slab 1, eligible for green rebate
        ("February", 140.0),  # Slab 2, green rebate
        ("March", 210.0),     # Slab 3, moderate increase (+50%) -> Spike
        ("April", 460.0),     # Slab 4, surcharge applied (> Rs 1500) -> Spike (+119%)
        ("May", 480.0),       # High summer consumption
        ("June", 180.0)       # Drop post-summer
    ]
    
    bills = process_monthly_billing(monthly_data)
    display_billing_statement(consumer, bills)


if __name__ == "__main__":
    run_demo()
