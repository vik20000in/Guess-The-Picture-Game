# Additional Vehicles
# Format: English Name | Hindi Name | Search Query

$additionalVehicles = @(
    @{ english = "Van"; hindi = "वैन"; search = "van vehicle" },
    @{ english = "Crane"; hindi = "क्रेन"; search = "construction crane vehicle" },
    @{ english = "Bulldozer"; hindi = "बुलडोजर"; search = "bulldozer construction vehicle" },
    @{ english = "Excavator"; hindi = "खुदाई मशीन"; search = "excavator digger machine" },
    @{ english = "Forklift"; hindi = "फोर्कलिफ्ट"; search = "forklift warehouse vehicle" },
    @{ english = "Golf Cart"; hindi = "गोल्फ कार्ट"; search = "golf cart vehicle" },
    @{ english = "Rickshaw"; hindi = "रिक्शा"; search = "cycle rickshaw india" },
    @{ english = "Yacht"; hindi = "नौका"; search = "luxury yacht boat" },
    @{ english = "Submarine"; hindi = "पनडुब्बी"; search = "submarine underwater vessel" },
    @{ english = "Hot Air Balloon"; hindi = "गर्म हवा का गुब्बारा"; search = "hot air balloon" },
    @{ english = "Hovercraft"; hindi = "होवरक्राफ्ट"; search = "hovercraft vehicle" },
    @{ english = "Snowmobile"; hindi = "स्नोमोबाइल"; search = "snowmobile snow vehicle" },
    @{ english = "ATV"; hindi = "एटीवी"; search = "ATV quad bike all terrain" },
    @{ english = "Segway"; hindi = "सेगवे"; search = "segway personal transporter" },
    @{ english = "Cable Car"; hindi = "केबल कार"; search = "cable car ropeway" }
)

# Run the setup script
.\setup_category.ps1 -CategoryName "vehicles" -Items $additionalVehicles
