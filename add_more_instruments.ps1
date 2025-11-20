# Additional Musical Instruments
# Format: English Name | Hindi Name | Search Query

$additionalInstruments = @(
    @{ english = "Bongo Drums"; hindi = "बोंगो ड्रम"; search = "bongo drums percussion" },
    @{ english = "Cymbals"; hindi = "झांझ"; search = "cymbals percussion instrument" },
    @{ english = "Tambourine"; hindi = "खंजरी"; search = "tambourine percussion instrument" },
    @{ english = "Maracas"; hindi = "मराकास"; search = "maracas shaker instrument" },
    @{ english = "Ukulele"; hindi = "युकेलेले"; search = "ukulele hawaiian guitar" },
    @{ english = "Bagpipes"; hindi = "बैगपाइप"; search = "bagpipes scottish instrument" },
    @{ english = "Oboe"; hindi = "ओबो"; search = "oboe woodwind instrument" },
    @{ english = "French Horn"; hindi = "फ्रेंच हॉर्न"; search = "french horn brass instrument" },
    @{ english = "Tuba"; hindi = "टूबा"; search = "tuba brass instrument" },
    @{ english = "Synthesizer"; hindi = "सिंथेसाइज़र"; search = "synthesizer keyboard electronic" },
    @{ english = "Electric Guitar"; hindi = "इलेक्ट्रिक गिटार"; search = "electric guitar rock" },
    @{ english = "Bass Guitar"; hindi = "बास गिटार"; search = "bass guitar instrument" },
    @{ english = "Bansuri"; hindi = "बांसुरी"; search = "bansuri bamboo flute indian" },
    @{ english = "Pakhawaj"; hindi = "पखावज"; search = "pakhawaj indian drum" },
    @{ english = "Ektara"; hindi = "एकतारा"; search = "ektara one string instrument india" }
)

# Run the setup script
.\setup_category.ps1 -CategoryName "instruments" -Items $additionalInstruments
