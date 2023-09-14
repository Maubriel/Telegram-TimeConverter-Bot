zones = {

    'paraguay':'America/Asuncion',
    'pry':'America/Asuncion',
    'py':'America/Asuncion',
    '🇵🇾':'America/Asuncion',

    'argentina':'America/Buenos_Aires',
    'arg':'America/Buenos_Aires',
    'ar':'America/Buenos_Aires',
    '🇦🇷':'America/Buenos_Aires',

    'colombia':'America/Bogota',
    'col':'America/Bogota',
    'co':'America/Bogota',
    '🇨🇴':'America/Bogota',

    'españa':'Europe/Madrid',
    'esp':'Europe/Madrid',
    'es':'Europe/Madrid',
    '🇪🇸':'Europe/Madrid',

    'mexico':'America/Mexico_City',
    'mex':'America/Mexico_City',
    'mx':'America/Mexico_City',
    '🇲🇽':'America/Mexico_City',

    'chile':'America/Santiago',
    'chl':'America/Santiago',
    'cl':'America/Santiago',
    '🇨🇱':'America/Santiago',

    'venezuela':'America/Caracas',
    'ven':'America/Caracas',
    've':'America/Caracas',
    '🇻🇪':'America/Caracas',

    'panama':'America/Panama',
    'pan':'America/Panama',
    'pa':'America/Panama',
    '🇵🇦':'America/Panama',

    'peru':'America/Lima',
    'per':'America/Lima',
    'pe':'America/Lima',
    '🇵🇪':'America/Lima',

    'el salvador':'America/El_Salvador',
    'slv':'America/El_Salvador',
    'sv':'America/El_Salvador',
    '🇸🇻':'America/El_Salvador',

    'ecuador':'America/Guayaquil',
    'ecu':'America/Guayaquil',
    'ec':'America/Guayaquil',
    '🇪🇨':'America/Guayaquil',

    'puerto rico':'America/Puerto_Rico',
    'pri':'America/Puerto_Rico',
    'pr':'America/Puerto_Rico',
    '🇵🇷':'America/Puerto_Rico',

    'honduras':'America/Tegucigalpa',
    'hnd':'America/Tegucigalpa',
    'hn':'America/Tegucigalpa',
    '🇭🇳':'America/Tegucigalpa',

    'bolivia':'America/La_Paz',
    'bol':'America/La_Paz',
    'bo':'America/La_Paz',
    '🇧🇴':'America/La_Paz',

    'uruguay':'America/Montevideo',
    'ury':'America/Montevideo',
    'uy':'America/Montevideo',
    '🇺🇾':'America/Montevideo',

    'cuba':'America/Havana',
    'cub':'America/Havana',
    'cu':'America/Havana',
    '🇨🇺':'America/Havana',

    'republica dominicana':'America/Santo_Domingo',
    'dom':'America/Santo_Domingo',
    'do':'America/Santo_Domingo',
    '🇩🇴':'America/Santo_Domingo',

    'nicaragua':'America/Managua',
    'nic':'America/Managua',
    'ni':'America/Managua',
    '🇳🇮':'America/Managua',

    'guatemala':'America/Guatemala',
    'gtm':'America/Guatemala',
    'gt':'America/Guatemala',
    '🇬🇹':'America/Guatemala',

    'costa rica':'America/Costa_Rica',
    'cri':'America/Costa_Rica',
    'cr':'America/Costa_Rica',
    '🇨🇷':'America/Costa_Rica',

    'guinea ecuatorial':'Africa/Malabo',
    'gnq':'Africa/Malabo',
    'gq':'Africa/Malabo',
    '🇬🇶':'Africa/Malabo',

}

paises = {
    'America/Asuncion':'PRY 🇵🇾',
    'America/Buenos_Aires':'ARG 🇦🇷',
    'America/Bogota':'COL 🇨🇴',
    'Europe/Madrid':'ESP 🇪🇸',
    'America/Mexico_City':'MEX 🇲🇽',
    'America/Santiago':'CHL 🇨🇱',
    'America/Caracas':'VEN 🇻🇪',
    'America/Panama':'PAN 🇵🇦',
    'America/Lima':'PER 🇵🇪',
    'America/El_Salvador':'SLV 🇸🇻',
    'America/Guayaquil':'ECU 🇪🇨',
    'America/Puerto_Rico':'PRI 🇵🇷',
    'America/Tegucigalpa':'HND 🇭🇳',
    'America/La_Paz':'BOL 🇧🇴',
    'America/Montevideo':'URY 🇺🇾',
    'America/Havana':'CUB 🇨🇺',
    'America/Santo_Domingo':'DOM 🇩🇴',
    'America/Managua':'NIC 🇳🇮',
    'America/Guatemala':'GTM 🇬🇹',
    'America/Costa_Rica':'CRI 🇨🇷',
    'Africa/Malabo':'GNQ 🇬🇶',
}

def get_timezone(code):
    try:
        cod = zones[code]
        return cod
    except KeyError:
        return ''

def get_pais(zone):
    try:
        pais = paises[zone]
        return pais
    except KeyError:
        return ''
