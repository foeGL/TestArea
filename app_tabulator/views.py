from django.shortcuts import render

# Create your views here.
def index(request):
    print("starte")
    tests = {
        2136: {
            'name': 'TE01',
            'formatted': 'TE01 - 47 CFR Part 15 - CE [Geleitete Störgrößen] [0,15 - 30 MHz][#38]',
            'standard': '47 CFR Part 15 Subpart B'}, 
        2137: {
            'name': 'TE02',
            'formatted': 'TE02 - 47 CFR Part 15 - RE [E-Feld][Vormessung SAC 3m][30 - 1000 MHz][#27]',
            'standard': '47 CFR Part 15 Subpart B'},
        2138: {
            'name': 'TE03',
            'formatted': 'TE03 - 47 CFR Part 15 - RE [E-Feld][Nachmessung OATS 10m][30 - 1000 MHz][#27]',
            'standard': '47 CFR Part 15 Subpart B'},
        2139: {
            'name': 'TE04',
            'formatted': 'TE04 - 47 CFR Part 15 - RE [E-Feld][SAC 3m][1 - 5 GHz][#27]',
            'standard': '47 CFR Part 15 Subpart B'},
        2140: {
            'name': 'TE05',
            'formatted': 'TE05 - 47 CFR Part 15 - Zulassungsverfahren Certification CAB/USA [#38]',
            'standard': '47 CFR Part 15 Subpart B'},
        2141: {
            'name': 'TE06',
            'formatted': 'TE06 - 47 CFR Part 15 - Zulassungskosten TCB - nach Aufwand [#38]',
            'standard': '47 CFR Part 15 Subpart B'},
        2142: {
            'name': 'TE07',
            'formatted': 'TE07 - Ergebnisbericht nach DIN EN ISO/IEC 17025:2018-03 - FCC - englisch',
            'standard': ''
            }
        }


    tableData = {
        0: {
            'ProtocolIdent': 684,
            'TestIdent': 2136,
            'OrderIdent': 448,
            'Operator': 'sv',
            'PersonelIdent': 7279, 
            'Date': '2021-10-06',
            'Start': '08:30',
            'Stop': '12:00',
            'TotalTime': 3.5,
            'InvoiceType': 1,
            'InvoiceStatus': '',
            'isTestFinished': True,
            'Comment': ''},
        1: {
            'ProtocolIdent': 685,
            'TestIdent': 2137,
            'OrderIdent': 448,
            'Operator': 'sv',
            'PersonelIdent': 7279,
            'Date': '2021-10-06',
            'Start': '14:45',
            'Stop': '16:30',
            'TotalTime': 2.0,
            'InvoiceType': 1,
            'InvoiceStatus': '',
            'isTestFinished': True,
            'Comment': ''},
        2: {
            'ProtocolIdent': 695,
            'TestIdent': 2138,
            'OrderIdent': 448,
            'Operator': 'sv',
            'PersonelIdent': 7279,
            'Date': '2021-10-07',
            'Start': '10:00',
            'Stop': '11:00',
            'TotalTime': 1.0,
            'InvoiceType': 1,
            'InvoiceStatus': '',
            'isTestFinished': False,
            'Comment': 'Aufbau'},
        3: {
            'ProtocolIdent': 704,
            'TestIdent': 2138,
            'OrderIdent': 448,
            'Operator': 'sv',
            'PersonelIdent': 7279,
            'Date': '2021-10-07',
            'Start': '11:00',
            'Stop': '12:00',
            'TotalTime': 1.0,
            'InvoiceType': 1,
            'InvoiceStatus': '',
            'isTestFinished': False,
            'Comment': ''},
        4: {
            'ProtocolIdent': 705,
            'TestIdent': 2138,
            'OrderIdent': 448,
            'Operator': 'sv',
            'PersonelIdent': 7279,
            'Date': '2021-10-07',
            'Start': '13:00',
            'Stop': '14:30',
            'TotalTime': 1.5,
            'InvoiceType': 1,
            'InvoiceStatus': '',
            'isTestFinished': True,
            'Comment': ''},
        5: {
            'ProtocolIdent': 687,
            'TestIdent': 2139,
            'OrderIdent': 448,
            'Operator': 'sv',
            'PersonelIdent': 7279,
            'Date': '2021-10-06',
            'Start': '17:00',
            'Stop': '17:50',
            'TotalTime': 1.0,
            'InvoiceType': 1,
            'InvoiceStatus': '',
            'isTestFinished': True,
            'Comment': ''},
        6: {
            'ProtocolIdent': 750,
            'TestIdent': 2142,
            'OrderIdent': 448,
            'Operator': 'sv',
            'PersonelIdent': 7279,
            'Date': '2021-10-11',
            'Start': '00:00',
            'Stop': '00:00',
            'TotalTime': 0.0,
            'InvoiceType': 0,
            'InvoiceStatus': '',
            'isTestFinished': False,
            'Comment': ''}
        }

    data = {
        'protocol': tableData, 
        'tests': tests, 
    }
    print("rendern")
    return render(request, "app_tabulator/templates/index.html", data)