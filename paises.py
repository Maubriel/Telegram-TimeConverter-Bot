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
    'GNQ':'Africa/Malabo',
    'GQ':'Africa/Malabo',
    '🇬🇶':'Africa/Malabo',

}

paises = {
    'America/Asuncion':'Paraguay 🇵🇾',
    'America/Buenos_Aires':'Argentina 🇦🇷',
    'America/Bogota':'Colombia 🇨🇴',
    'Europe/Madrid':'España 🇪🇸',
    'America/Mexico_City':'México 🇲🇽',
    'America/Santiago':'Chile 🇨🇱',
    'America/Panama':'Panamá 🇵🇦',
    'America/Caracas':'Venezuela 🇻🇪',
    'America/Lima':'Perú 🇵🇪',
    'America/El_Salvador':'El Salvador 🇸🇻',
    'America/Guayaquil':'Ecuador 🇪🇨',
    'America/Puerto_Rico':'Puerto Rico 🇵🇷',
    'America/Tegucigalpa':'Honduras 🇭🇳',
    'America/La_Paz':'Bolivia 🇧🇴',
    'America/Montevideo':'Uruguay 🇺🇾',
    'America/Havana':'Cuba 🇨🇺',
    'America/Santo_Domingo':'República Dominicana 🇩🇴',
    'America/Managua':'Nicaragua 🇳🇮',
    'America/Guatemala':'Guatemala 🇬🇹',
    'America/Costa_Rica':'Costa Rica 🇨🇷',
    'Africa/Malabo':'Guinea Ecuatorial 🇬🇶',
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
