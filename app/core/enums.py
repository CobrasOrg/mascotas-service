from enum import Enum

class SpeciesEnum(str, Enum):
    canine = "canine"
    feline = "feline"

class BloodTypeEnum(str, Enum):
    DEA_1_1_pos = "DEA 1.1+"
    DEA_1_1_neg = "DEA 1.1-"
    A = "A"
    B = "B"
    AB = "AB"

BREEDS = {
    "canine": [
        "Golden Retriever", "Labrador Retriever", "Pastor Alemán", "Bulldog Francés",
        "Poodle", "Rottweiler", "Yorkshire Terrier", "Beagle", "Husky Siberiano",
        "Chihuahua", "Mestizo", "Otro"
    ],
    "feline": [
        "Siamés", "Persa", "Maine Coon", "Británico de Pelo Corto", "Ragdoll",
        "Bengalí", "Abisinio", "Sphynx", "Mestizo", "Otro"
    ],
}
