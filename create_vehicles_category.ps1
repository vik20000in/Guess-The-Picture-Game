# Vehicles Category Data
# Format: English Name | Hindi Name | Search Query

$vehicleItems = @(
    @{ english = "Car"; hindi = "कार"; search = "car vehicle" },
    @{ english = "Bus"; hindi = "बस"; search = "bus public transport" },
    @{ english = "Train"; hindi = "ट्रेन"; search = "train locomotive" },
    @{ english = "Airplane"; hindi = "हवाई जहाज"; search = "airplane aircraft" },
    @{ english = "Bicycle"; hindi = "साइकिल"; search = "bicycle bike" },
    @{ english = "Motorcycle"; hindi = "मोटरसाइकिल"; search = "motorcycle motorbike" },
    @{ english = "Truck"; hindi = "ट्रक"; search = "truck lorry" },
    @{ english = "Auto Rickshaw"; hindi = "ऑटो रिक्शा"; search = "auto rickshaw india" },
    @{ english = "Boat"; hindi = "नाव"; search = "boat ship" },
    @{ english = "Helicopter"; hindi = "हेलीकॉप्टर"; search = "helicopter aircraft" },
    @{ english = "Scooter"; hindi = "स्कूटर"; search = "scooter moped" },
    @{ english = "Taxi"; hindi = "टैक्सी"; search = "yellow taxi cab" },
    @{ english = "Ambulance"; hindi = "एम्बुलेंस"; search = "ambulance emergency vehicle" },
    @{ english = "Fire Truck"; hindi = "दमकल"; search = "fire truck engine" },
    @{ english = "Police Car"; hindi = "पुलिस कार"; search = "police car vehicle" },
    @{ english = "Tractor"; hindi = "ट्रैक्टर"; search = "tractor farm vehicle" },
    @{ english = "Metro"; hindi = "मेट्रो"; search = "metro train subway" },
    @{ english = "Ship"; hindi = "जहाज"; search = "ship cargo vessel" },
    @{ english = "Rocket"; hindi = "रॉकेट"; search = "rocket spacecraft" },
    @{ english = "Jeep"; hindi = "जीप"; search = "jeep SUV vehicle" }
)

# Run the setup script
.\setup_category.ps1 -CategoryName "vehicles" -Items $vehicleItems
