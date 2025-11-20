# Musical Instruments Category Data
# Format: English Name | Hindi Name | Search Query

$instrumentItems = @(
    @{ english = "Guitar"; hindi = "गिटार"; search = "acoustic guitar musical instrument" },
    @{ english = "Piano"; hindi = "पियानो"; search = "piano keyboard instrument" },
    @{ english = "Drum"; hindi = "ढोल"; search = "drum percussion instrument" },
    @{ english = "Flute"; hindi = "बांसुरी"; search = "flute bamboo instrument" },
    @{ english = "Violin"; hindi = "वायलिन"; search = "violin string instrument" },
    @{ english = "Tabla"; hindi = "तबला"; search = "tabla indian drums" },
    @{ english = "Harmonium"; hindi = "हारमोनियम"; search = "harmonium indian instrument" },
    @{ english = "Sitar"; hindi = "सितार"; search = "sitar indian instrument" },
    @{ english = "Trumpet"; hindi = "तुरही"; search = "trumpet brass instrument" },
    @{ english = "Saxophone"; hindi = "सैक्सोफोन"; search = "saxophone musical instrument" },
    @{ english = "Veena"; hindi = "वीणा"; search = "veena indian string instrument" },
    @{ english = "Sarangi"; hindi = "सारंगी"; search = "sarangi indian instrument" },
    @{ english = "Dholak"; hindi = "ढोलक"; search = "dholak indian drum" },
    @{ english = "Shehnai"; hindi = "शहनाई"; search = "shehnai indian wind instrument" },
    @{ english = "Manjira"; hindi = "मंजीरा"; search = "manjira cymbals indian" },
    @{ english = "Mridangam"; hindi = "मृदंगम"; search = "mridangam south indian drum" },
    @{ english = "Ghatam"; hindi = "घटम"; search = "ghatam clay pot instrument" },
    @{ english = "Banjo"; hindi = "बैंजो"; search = "banjo string instrument" },
    @{ english = "Accordion"; hindi = "अकॉर्डियन"; search = "accordion musical instrument" },
    @{ english = "Harp"; hindi = "वीणा"; search = "harp string instrument" },
    @{ english = "Xylophone"; hindi = "जाइलोफोन"; search = "xylophone percussion instrument" },
    @{ english = "Clarinet"; hindi = "शहनाई"; search = "clarinet woodwind instrument" },
    @{ english = "Trombone"; hindi = "ट्रॉम्बोन"; search = "trombone brass instrument" },
    @{ english = "Cello"; hindi = "सेलो"; search = "cello string instrument" },
    @{ english = "Double Bass"; hindi = "कॉन्ट्राबास"; search = "double bass string instrument" }
)

# Run the setup script
.\setup_category.ps1 -CategoryName "instruments" -Items $instrumentItems
