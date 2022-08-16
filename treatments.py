#!/usr/bin/python3

"""docstring goes here"""

# Definitions of treatments
CNTL = "Control"
SHAM = "SHAM 100 ug/mL"
AZX1 = "Azoxystrobin 10 ug/mL"
BOS1 = "Boscalid 1 ug/mL"
BOS2 = "Boscalid 10 ug/mL"
BOS3 = "Boscalid 100 ug/mL"
FLU1 = "Fluopyram 1 ug/mL"
FLU2 = "Fluopyram 10 ug/mL"
FLU3 = "Fluopyram 100 ug/mL"
MCB1 = "Myclobutanil 25 ug/mL"
MCB2 = "Myclobutanil 250 ug/mL"
MCB3 = "Myclobutanil 2500 ug/mL"
TEB1 = "Tebuconazole 25 ug/mL"
TEB2 = "Tebuconazole 250 ug/mL"
TEB3 = "Tebuconazole 2500 ug/mL"
DFC1 = "Difenoconazole 25 ug/mL"
DFC2 = "Difenoconazole 250 ug/mL"
DFC3 = "Difenoconazole 2500 ug/mL"
FTF1 = "Flutriafol 25 ug/mL"
FTF2 = "Flutriafol 250 ug/mL"
FTF3 = "Flutriafol 2500 ug/mL"
QXF1 = "Quinoxyfen 0.01 ug/mL"
QXF2 = "Quinoxyfen 0.1 ug/mL"
QXF3 = "Quinoxyfen 1 ug/mL"

# maps of treatment blocks
def get_treatments(plate, block):
    """docstring goes here"""
    if plate == "plate1a":
        # Isolates: LH1, MEN8B
        treatments = [
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
        ]
    elif plate == "plate1b":
        # Isolates: LH1, MEN8B
        treatments = [
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
        ]
    elif plate == "plate2a":
        # Isolates: SC4SY-B, MICV3
        treatments = [
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
        ]
    elif plate == "plate2b":
        # Isolates: SC4SY-B, MICV3
        treatments = [
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
        ]
    elif plate == "plate3a":
        # Isolate: DDO-ME-2
        treatments = [
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
        ]
    elif plate == "plate3b":
        # Isolate: DDO-ME-2
        treatments = [
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
        ]
    elif plate == "plate4a":
        # Isolate: GAT1
        treatments = [
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
        ]
    elif plate == "plate4b":
        # Isolate: GAT1 (48 hr images are missing for this plate + isolate.)
        treatments = []
    elif plate == "plate5a":
        # Isolates: KRAE1B, NAPA02-T
        treatments = [
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
        ]
    elif plate == "plate5b":
        # Isolates: KRAE1B, NAPA02-T
        treatments = [
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
        ]
    elif plate == "plate6a":
        # Isolates: R532ST190-1, NAPA05-PB
        treatments = [
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
        ]
    elif plate == "plate6b":
        # Isolates: R532ST190-1, NAPA05-PB
        treatments = [
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
        ]
    elif plate == "plate7a":
        # Isolates: GAT1, PFV-6A
        treatments = [
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
        ]
    elif plate == "plate7b":
        # Isolates: GAT1, PFV-6A
        treatments = [
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
        ]
    elif plate == "plate8a":
        # Isolates: HO2, SE-22B
        treatments = [
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
        ]
    elif plate == "plate8b":
        # Isolates: HO2, SE-22B
        treatments = [
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
        ]
    elif plate == "plate9a":
        # Isolate: CAL3B
        treatments = [
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
        ]
    elif plate == "plate9b":
        # Isolate: CAL3B
        treatments = [
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
        ]
    elif plate == "plate10a":
        # Isolate: MITG2
        treatments = [
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
        ]
    elif plate == "plate10b":
        # Isolate: MITG2
        treatments = [
            FLU1, FLU1, FLU1, FLU1,
            FLU2, FLU2, FLU2, FLU2,
            FLU3, FLU3, FLU3, FLU3,
            DFC1, DFC1, DFC1, DFC1,
            DFC2, DFC2, DFC2, DFC2,
            DFC3, DFC3, DFC3, DFC3,
            QXF1, QXF1, QXF1, QXF1,
            QXF2, QXF2, QXF2, QXF2,
            QXF3, QXF3, QXF3, QXF3,
            TEB1, TEB1, TEB1, TEB1,
            TEB2, TEB2, TEB2, TEB2,
            TEB3, TEB3, TEB3, TEB3,
            BOS1, BOS1, BOS1, BOS1,
            BOS2, BOS2, BOS2, BOS2,
            BOS3, BOS3, BOS3, BOS3,
            CNTL, CNTL, CNTL, CNTL,
            SHAM, SHAM, SHAM, SHAM,
            AZX1, AZX1, AZX1, AZX1,
            MCB1, MCB1, MCB1, MCB1,
            MCB2, MCB2, MCB2, MCB2,
            MCB3, MCB3, MCB3, MCB3,
            FTF1, FTF1, FTF1, FTF1,
            FTF2, FTF2, FTF2, FTF2,
            FTF3, FTF3, FTF3, FTF3,
        ]
    return treatments[block]
