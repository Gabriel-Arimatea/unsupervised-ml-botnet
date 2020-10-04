DATASETS = [
    'Danmini_Doorbell',
    'Ecobee_Thermostat',
    'Ennio_Doorbell',
    'Philips_B120N10_Baby_Monitor',
    'Provision_PT_737E_Security_Camera',
    'Provision_PT_838_Security_Camera',
    'Samsung_SNH_1011_N_Webcam',
    'SimpleHome_XCS7_1002_WHT_Security_Camera',
    'SimpleHome_XCS7_1003_WHT_Security_Camera'
]

DATASETS_DISPONIVEIS = {
    'BASE_PATH': 'D:\\Users\\Gabriel\\Downloads\\Datasets\\N-BaIoT\\',
    'BASE_SCHEMA': 'demonstrate_structure.csv',
    'Danmini_Doorbell': {
        'descricao': 'Danmini_Doorbell: Mirai e Bashlite', 
        'benign': 'benign_traffic.csv',
        'attacks': [
            'scan_1.csv',
            'scan.csv'
        ]
    },
    'Ecobee_Thermostat': {
        'descricao': 'Ecobee_Thermostat: Mirai e Bashlite', 
        'benign': 'benign_traffic.csv',
        'attacks': [
            'et_scan_1.csv',
            'et_scan.csv'
        ]
    },
    'Ennio_Doorbell': {
        'descricao': 'Ennio_Doorbell: Bashlite',
        'benign': 'benign_traffic.csv',
        'attacks': [
            'ed_scan.csv'
        ]
    },
    'Philips_B120N10_Baby_Monitor': {
        'descricao': 'Philips_B120N10_Baby_Monitor: Mirai e Bashlite',
        'benign': 'benign_traffic.csv',
        'attacks': [
            'p1_scan_1.csv',
            'p1_scan.csv'
        ]
    },
    'Provision_PT_737E_Security_Camera': {
        'descricao': 'Provision_PT_737E_Security_Camera: Mirai e Bashlite',
        'benign': 'benign_traffic.csv',
        'attacks': [
            'p2_scan_1.csv',
            'p2_scan.csv'
        ]
    },
    'Provision_PT_838_Security_Camera': {
        'descricao': 'Provision_PT_838_Security_Camera: Mirai e Bashlite',
        'benign': 'benign_traffic.csv',
        'attacks': [
            'p3_scan_1.csv',
            'p3_scan.csv'
        ]
    },
    'Samsung_SNH_1011_N_Webcam': {
        'descricao': 'Samsung_SNH_1011_N_Webcam: Bashlite',
        'benign': 'benign_traffic.csv',
        'attacks': [
            's1_scan.csv'
        ]
    },
    'SimpleHome_XCS7_1002_WHT_Security_Camera': {
        'descricao': 'SimpleHome_XCS7_1002_WHT_Security_Camera: Mirai e Bashlite',
        'benign': 'benign_traffic.csv',
        'attacks': [
            's2_scan_1.csv',
            's2_scan.csv'
        ]
    },
    'SimpleHome_XCS7_1003_WHT_Security_Camera': {
        'descricao': 'SimpleHome_XCS7_1003_WHT_Security_Camera: Mirai e Bashlite',
        'benign': 'benign_traffic.csv',
        'attacks': [
            's3_scan_1.csv',
            's3_scan.csv'
        ]
    }
}
