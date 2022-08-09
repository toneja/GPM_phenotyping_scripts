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
    if plate == "plate6a":
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
            BOS3, BOS3, BOS3, BOS3
        ]
    elif plate == "plate6b":
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
            QXF3, QXF3, QXF3, QXF3
        ]

    return treatments[block]
