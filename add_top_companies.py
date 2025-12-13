"""
Add top 100 paying companies, especially VLSI companies, to the database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credmarket.settings')
django.setup()

from companies.models import Company
from accounts.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

# Get or create admin user for adding companies
admin_user = User.objects.filter(is_superuser=True).first()
if not admin_user:
    admin_user = User.objects.filter(is_staff=True).first()

# Top 100 paying companies with focus on VLSI/Semiconductor
companies_data = [
    # VLSI & Semiconductor Companies
    ('Cadence Design Systems', 'cadence.com', 'https://www.cadence.com', 'Leading EDA software provider'),
    ('Synopsys', 'synopsys.com', 'https://www.synopsys.com', 'EDA and semiconductor IP company'),
    ('Qualcomm', 'qualcomm.com', 'https://www.qualcomm.com', 'Wireless technology and semiconductors'),
    ('NVIDIA', 'nvidia.com', 'https://www.nvidia.com', 'GPU and AI chip manufacturer'),
    ('Intel', 'intel.com', 'https://www.intel.com', 'Semiconductor chip manufacturer'),
    ('AMD', 'amd.com', 'https://www.amd.com', 'Processor and graphics manufacturer'),
    ('Broadcom', 'broadcom.com', 'https://www.broadcom.com', 'Semiconductor and infrastructure software'),
    ('Texas Instruments', 'ti.com', 'https://www.ti.com', 'Semiconductor design and manufacturing'),
    ('Analog Devices', 'analog.com', 'https://www.analog.com', 'Analog, mixed-signal and DSP integrated circuits'),
    ('Marvell Technology', 'marvell.com', 'https://www.marvell.com', 'Semiconductor company'),
    ('NXP Semiconductors', 'nxp.com', 'https://www.nxp.com', 'Automotive and IoT semiconductors'),
    ('Microchip Technology', 'microchip.com', 'https://www.microchip.com', 'Microcontroller and semiconductor'),
    ('Applied Materials', 'appliedmaterials.com', 'https://www.appliedmaterials.com', 'Semiconductor equipment'),
    ('ASML', 'asml.com', 'https://www.asml.com', 'Semiconductor equipment manufacturer'),
    ('Lam Research', 'lamresearch.com', 'https://www.lamresearch.com', 'Semiconductor equipment'),
    ('KLA Corporation', 'kla.com', 'https://www.kla.com', 'Process control and yield management'),
    ('Mentor Graphics', 'mentor.com', 'https://www.mentor.com', 'EDA software (Siemens)'),
    ('Xilinx', 'xilinx.com', 'https://www.xilinx.com', 'FPGA manufacturer (AMD)'),
    ('Altera', 'altera.com', 'https://www.altera.com', 'FPGA manufacturer (Intel)'),
    ('Renesas Electronics', 'renesas.com', 'https://www.renesas.com', 'Semiconductor manufacturer'),
    ('STMicroelectronics', 'st.com', 'https://www.st.com', 'Semiconductor company'),
    ('Infineon Technologies', 'infineon.com', 'https://www.infineon.com', 'Semiconductor solutions'),
    ('ON Semiconductor', 'onsemi.com', 'https://www.onsemi.com', 'Power and sensing semiconductors'),
    ('Maxim Integrated', 'maximintegrated.com', 'https://www.maximintegrated.com', 'Analog and mixed-signal products'),
    ('Lattice Semiconductor', 'latticesemi.com', 'https://www.latticesemi.com', 'Low power FPGA'),
    
    # Tech Giants
    ('Google', 'google.com', 'https://www.google.com', 'Technology and internet services'),
    ('Microsoft', 'microsoft.com', 'https://www.microsoft.com', 'Software and cloud services'),
    ('Apple', 'apple.com', 'https://www.apple.com', 'Consumer electronics and software'),
    ('Amazon', 'amazon.com', 'https://www.amazon.com', 'E-commerce and cloud computing'),
    ('Meta', 'meta.com', 'https://www.meta.com', 'Social media and technology'),
    ('Netflix', 'netflix.com', 'https://www.netflix.com', 'Streaming entertainment'),
    ('Salesforce', 'salesforce.com', 'https://www.salesforce.com', 'Cloud-based CRM'),
    ('Oracle', 'oracle.com', 'https://www.oracle.com', 'Database and cloud solutions'),
    ('Adobe', 'adobe.com', 'https://www.adobe.com', 'Creative and marketing software'),
    ('SAP', 'sap.com', 'https://www.sap.com', 'Enterprise software'),
    ('IBM', 'ibm.com', 'https://www.ibm.com', 'Cloud and AI solutions'),
    ('Cisco', 'cisco.com', 'https://www.cisco.com', 'Networking and security'),
    ('VMware', 'vmware.com', 'https://www.vmware.com', 'Cloud infrastructure'),
    ('ServiceNow', 'servicenow.com', 'https://www.servicenow.com', 'Digital workflow platform'),
    
    # Consulting & Services
    ('Accenture', 'accenture.com', 'https://www.accenture.com', 'Management consulting and technology'),
    ('Deloitte', 'deloitte.com', 'https://www.deloitte.com', 'Professional services'),
    ('PwC', 'pwc.com', 'https://www.pwc.com', 'Professional services'),
    ('EY', 'ey.com', 'https://www.ey.com', 'Professional services'),
    ('KPMG', 'kpmg.com', 'https://www.kpmg.com', 'Professional services'),
    ('McKinsey', 'mckinsey.com', 'https://www.mckinsey.com', 'Management consulting'),
    ('BCG', 'bcg.com', 'https://www.bcg.com', 'Management consulting'),
    ('Bain', 'bain.com', 'https://www.bain.com', 'Management consulting'),
    ('Capgemini', 'capgemini.com', 'https://www.capgemini.com', 'Consulting and technology'),
    ('Cognizant', 'cognizant.com', 'https://www.cognizant.com', 'IT services and consulting'),
    
    # Finance & Fintech
    ('Goldman Sachs', 'goldmansachs.com', 'https://www.goldmansachs.com', 'Investment banking'),
    ('Morgan Stanley', 'morganstanley.com', 'https://www.morganstanley.com', 'Investment banking'),
    ('JP Morgan Chase', 'jpmorganchase.com', 'https://www.jpmorganchase.com', 'Banking and financial services'),
    ('Citi', 'citi.com', 'https://www.citi.com', 'Banking and financial services'),
    ('Bank of America', 'bankofamerica.com', 'https://www.bankofamerica.com', 'Banking services'),
    ('American Express', 'americanexpress.com', 'https://www.americanexpress.com', 'Financial services'),
    ('Visa', 'visa.com', 'https://www.visa.com', 'Payment technology'),
    ('Mastercard', 'mastercard.com', 'https://www.mastercard.com', 'Payment technology'),
    ('PayPal', 'paypal.com', 'https://www.paypal.com', 'Online payment systems'),
    ('Bloomberg', 'bloomberg.com', 'https://www.bloomberg.com', 'Financial data and media'),
    
    # E-commerce & Retail
    ('Walmart', 'walmart.com', 'https://www.walmart.com', 'Retail and e-commerce'),
    ('Flipkart', 'flipkart.com', 'https://www.flipkart.com', 'E-commerce platform'),
    ('Myntra', 'myntra.com', 'https://www.myntra.com', 'Fashion e-commerce'),
    ('Swiggy', 'swiggy.com', 'https://www.swiggy.com', 'Food delivery platform'),
    ('Zomato', 'zomato.com', 'https://www.zomato.com', 'Food delivery and restaurant discovery'),
    ('Uber', 'uber.com', 'https://www.uber.com', 'Ride-sharing and delivery'),
    ('Ola', 'olacabs.com', 'https://www.olacabs.com', 'Ride-sharing platform'),
    
    # Startups & Unicorns
    ('Paytm', 'paytm.com', 'https://www.paytm.com', 'Digital payments and financial services'),
    ('PhonePe', 'phonepe.com', 'https://www.phonepe.com', 'Digital payments'),
    ('Razorpay', 'razorpay.com', 'https://www.razorpay.com', 'Payment gateway'),
    ('Freshworks', 'freshworks.com', 'https://www.freshworks.com', 'Business software'),
    ('Zoho', 'zoho.com', 'https://www.zoho.com', 'Business software'),
    ('BYJU''S', 'byjus.com', 'https://www.byjus.com', 'Education technology'),
    ('Unacademy', 'unacademy.com', 'https://www.unacademy.com', 'Education platform'),
    ('Dream11', 'dream11.com', 'https://www.dream11.com', 'Fantasy sports'),
    ('Ola Electric', 'olaelectric.com', 'https://www.olaelectric.com', 'Electric vehicles'),
    ('CRED', 'cred.club', 'https://www.cred.club', 'Credit card payment platform'),
    
    # Telecom
    ('Airtel', 'airtel.in', 'https://www.airtel.in', 'Telecommunications'),
    ('Jio', 'jio.com', 'https://www.jio.com', 'Telecommunications'),
    ('Vodafone Idea', 'myvi.in', 'https://www.myvi.in', 'Telecommunications'),
    
    # Automotive & Manufacturing
    ('Tesla', 'tesla.com', 'https://www.tesla.com', 'Electric vehicles and clean energy'),
    ('Ford', 'ford.com', 'https://www.ford.com', 'Automobile manufacturer'),
    ('General Motors', 'gm.com', 'https://www.gm.com', 'Automobile manufacturer'),
    ('Bosch', 'bosch.com', 'https://www.bosch.com', 'Engineering and technology'),
    ('Honeywell', 'honeywell.com', 'https://www.honeywell.com', 'Industrial technology'),
    ('GE', 'ge.com', 'https://www.ge.com', 'Industrial and digital solutions'),
    ('Siemens', 'siemens.com', 'https://www.siemens.com', 'Industrial manufacturing and automation'),
    
    # Aerospace & Defense
    ('Boeing', 'boeing.com', 'https://www.boeing.com', 'Aerospace manufacturer'),
    ('Lockheed Martin', 'lockheedmartin.com', 'https://www.lockheedmartin.com', 'Aerospace and defense'),
    ('Northrop Grumman', 'northropgrumman.com', 'https://www.northropgrumman.com', 'Aerospace and defense'),
    ('Raytheon', 'rtx.com', 'https://www.rtx.com', 'Aerospace and defense'),
    
    # Additional Tech Companies
    ('Slack', 'slack.com', 'https://www.slack.com', 'Business communication platform'),
    ('Atlassian', 'atlassian.com', 'https://www.atlassian.com', 'Team collaboration software'),
    ('Dropbox', 'dropbox.com', 'https://www.dropbox.com', 'Cloud storage and collaboration'),
    ('Zoom', 'zoom.us', 'https://www.zoom.us', 'Video communications'),
    ('Snowflake', 'snowflake.com', 'https://www.snowflake.com', 'Cloud data platform'),
    ('Databricks', 'databricks.com', 'https://www.databricks.com', 'Data and AI platform'),
    ('Palantir', 'palantir.com', 'https://www.palantir.com', 'Data analytics'),
]

print("Adding top paying companies to the database...\n")

added_count = 0
existing_count = 0

for name, domain, website, description in companies_data:
    # Check if company already exists
    if Company.objects.filter(domain=domain).exists():
        existing_count += 1
        print(f"⏭️  {name} ({domain}) - Already exists")
    else:
        company = Company.objects.create(
            name=name,
            domain=domain,
            website=website,
            description=description,
            status='approved',
            added_by=admin_user,
            approved_by=admin_user
        )
        added_count += 1
        print(f"✅ {name} ({domain}) - Added")

print(f"\n{'='*60}")
print(f"Summary:")
print(f"  ✅ Added: {added_count} companies")
print(f"  ⏭️  Skipped (already exists): {existing_count} companies")
print(f"  📊 Total in list: {len(companies_data)} companies")
print(f"{'='*60}")
print("\nDone! All top paying companies (especially VLSI) have been added to the database.")
