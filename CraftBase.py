

def gump(group, item):
    return [group, item]


resourcesId = {
    'Cloth': [0x1766], # 0x1767=uncut 0x1766=cut
    'Leather': [0x1081],
    
    'Iron': [0x1BF2],
    'Dull Copper': [0x1BF2],
    'Shadow': [0x1BF2],
    
    'RegularWood': [0x1BD7],
    'BowstringLeather': [0x1535],
    'Scale': [0x26B4],
    
    'Bone': [0x0F7E]
}

resourcesHue = {
    'Cloth': -1,
    
    'Leather': 0, # kolor podstawowy
    'Spined': 0x08ac,
    'Horned': 0x0845,
    'Barbed': 0x0851,
    
    'Iron': 0, # kolor podstawowy
    'Dull Copper': 0x0973,
    'Shadow': 0x0966,
    'Copper': 0x096d,
    'Bronze': 0x0972,
    'Golden': 0x08a5,
    'Agapite': 0x0979,
    'Verite': 0x089f,
    
    'RegularWood': 0,  # 0x059c = giętkie, 0x065b = opalone, 0x047f = zmarzniete, 0x0393 = skamieniale, 0x0709 = puste, 0x07da = zywiczne
    'Oak': 0x07da, # oak
    'Ash': 0x0709, # puste
    'Yew': 0x0393, # skamieniale
    'Heartwood': 0x059c, # gietkie
    'Bloodwood': 0x065b, # opalone
    'Frostwood': 0x047f, # zmarzniete
    
    'BowstringLeather': 0x046c,
    'BowstringGut': 0x0475,
    'BowstringCannabis': 0x048c,
    'BowstringSilk': 0x0b46,  
    
    'Scale': 0, # luski, TODO
    
    'Bone': 0,
}

tailorInternalBase = [
#   [Name, TypeId, [GumpGroup, GumpItem], [Rersource1Name, Resource1Amount], [Rersource2Name, Resource2Amount] ]
    #['nnnazwa',    0xffff, [99, 9999], ['Cloth', 33], []],
    
    ['mycka',   0x1544, gump(1, 2), ['Cloth', 2], []],
    ['bandana', 0x1540, gump(1, 9), ['Cloth', 2], []],
    ['kapelusz', 0x1713, gump(1, 16), ['Cloth', 11], []],
    ['czapka', 0x1715, gump(1, 23), ['Cloth', 11], []],
    ['szeroki kapelusz', 0x1714, gump(1, 30), ['Cloth', 12], []],
    ['slomkowy kapelusz', 0x1717, gump(1, 37), ['Cloth', 10], []],
    ['wysoki slomkowy kapelusz', 0x1716, gump(1, 44), ['Cloth', 13], []],
    ['kapelusz maga', 0x1718, gump(1, 51), ['Cloth', 15], []],
    ['beret', 0x1719, gump(1, 58), ['Cloth', 11], []],
    ['kapelusz z piorkiem', 0x171A, gump(1, 65), ['Cloth', 12], []],
    
    ['trojkatny kapelusz', 0x171B, gump(1, 72), ['Cloth', 12], []],
    ['czapka blazna', 0x171C, gump(1, 79), ['Cloth', 15], []],
    ['girlanda z kwiatow', 0x2306, gump(1, 86), ['Cloth', 5], []],
    ['maska', 0x278F, gump(1, 93), ['Cloth', 13], []],
    ['slomiany kapelusz', 0x2798, gump(1, 100), ['Cloth', 12], []],
    
    ['dublet',  0x1F7B, gump(8, 2), ['Cloth', 8], []],
    ['koszula', 0x1517, gump(8, 9), ['Cloth', 8], []],
    ['elegancka koszula', 0x3175, gump(8, 16), ['Cloth', 8], []],
    ['koszula z rekawami',  0x1EFD, gump(8, 23), ['Cloth', 8], []],
    ['tunika',  0x1FA1, gump(8, 30), ['Cloth', 12], []],
    ['oponcza', 0x1FFD, gump(8, 37), ['Cloth', 14], []],
    ['sukienka', 0x1F01, gump(8, 44), ['Cloth', 10], []],
    ['haftowana suknia', 0x1F00, gump(8, 51), ['Cloth', 12], []],
    ['plaszcz', 0x1515, gump(8, 58), ['Cloth', 14], []],
    ['szata', 0x1F03, gump(8, 65), ['Cloth', 16], []],
    # druga i trzecia strona do rewizji:
    #['elegancka szata z kapturem', 0xffff, gump(8, 72), ['Cloth', 33], []],
    #['elegancka szata', 0xffff, gump(8, 79), ['Cloth', 33], []],
    ['szata blazna',  0x1F9F, gump(8, 86), ['Cloth', 24], []],
    #['peleryna', 0xffff, gump(8, 93), ['Cloth', 33], []],
    #['gildiowa szata', 0xffff, gump(8, 100), ['Cloth', 33], []],
    #['ozdobna koszula', 0xffff, gump(8, 107), ['Cloth', 33], []],
    #['koszula', 0xffff, gump(8, 114), ['Cloth', 33], []],
    #['ciezka szata', 0xffff, gump(8, 121), ['Cloth', 33], []],
    #
    #['sukmana', 0xffff, gump(8, 128), ['Cloth', 33], []],
    #['toga', 0xffff, gump(8, 135), ['Cloth', 33], []],
    #['suknia', 0xffff, gump(8, 142), ['Cloth', 33], []],
    #['kamizelka', 0xffff, gump(8, 149), ['Cloth', 33], []],
    
    ['krotkie spodnie', 0x152E, gump(15, 2), ['Cloth', 6], []],
    ['eleganckie spodnie', 0x2FC3, gump(15, 9), ['Cloth', 6], []],
    ['dlugie spodnie', 0x1539, gump(15, 16), ['Cloth', 8], []],
    ['kilt', 0x1537, gump(15, 23), ['Cloth', 8], []],
    ['spodniczka', 0x1516, gump(15, 30), ['Cloth', 10], []],
    ['futrzany kilt', 0x230C, gump(15, 37), ['Cloth', 12], []],
    ['trzcinowa spodnica', 0x279A, gump(15, 44), ['Cloth', 16], []],
    ['szerokie spodnie', 0x279B, gump(15, 51), ['Cloth', 16], []],

    ['szarfa', 0x1541, gump(22, 2), ['Cloth', 4], []],
    #['lesny pas', 0xffff, gump(22, 9), ['Cloth', 33], []],
    ['krotki fartuch', 0x153B, gump(22, 16), ['Cloth', 6], []],
    ['dlugi fartuch', 0x153D, gump(22, 23), ['Cloth', 10], []],
    #['szeroki pas', 0xffff, gump(22, 30), ['Cloth', 33], []],
    
    #['futrzane buty', 0xffff, gump(29, 2), ['Leather', 33], []],
    #['zimowe buty', 0xffff, gump(29, 9), ['Leather', 33], []],
    #['letnie sandaly', 0xffff, gump(29, 16), ['Leather', 33], []],
    ['sandaly', 0x170D, gump(29, 23), ['Leather', 4], []],
    ['buciki', 0x170F, gump(29, 30), ['Leather', 6], []],
    ['buty', 0x170B, gump(29, 37), ['Leather', 8], []],
    ['wysokie buty', 0x1711, gump(29, 44), ['Leather', 10], []],
    #['eleganckie buty', 0xffff, gump(29, 51), ['Leather', 33], []],
    
    ['skorzany karczek', 0x13C7, gump(36, 2), ['Leather', 4], []],
    ['skorzana czapka', 0x1DB9, gump(36, 9), ['Leather', 2], []],
    ['skorzane rekawice', 0x13C6, gump(36, 16), ['Leather', 3], []],
    ['skorzane naramienniki', 0x13CD, gump(36, 23), ['Leather', 4], []],
    ['skorzane nogawice', 0x13CB, gump(36, 30), ['Leather', 10], []],
    ['skorzana tunika', 0x13CC, gump(36, 37), ['Leather', 12], []],
    
    ['skorzane spodenki', 0x1C00, gump(50, 2), ['Leather', 8], []],
    ['skorzana spodniczka', 0x1C08, gump(50, 9), ['Leather', 6], []],
    ['skorzany biustonosz', 0x1C0A, gump(50, 16), ['Leather', 6], []],
    ['skorzany utwardzany biustonosz', 0x1C0C, gump(50, 23), ['Leather', 8], []],
    ['kobieca skorzana zbroja', 0x1C06, gump(50, 30), ['Leather', 8], []],
    ['kobieca utwardzana skorzana zbroja', 0x1C02, gump(50, 37), ['Leather', 10], []],
    
    ['skorzany utwardzany karczek', 0x13D6, gump(43, 2), ['Leather', 6], []],
    ['skorzane utwardzane rekawice', 0x13D5, gump(43, 9), ['Leather', 8], []],
    ['skorzane utwardzane naramienniki', 0x13DC, gump(43, 16), ['Leather', 10], []],
    ['skorzane utwardzane nogawice', 0x13DA, gump(43, 23), ['Leather', 12], []],
    ['skorzana utwardzana tunika', 0x13DB, gump(43, 30), ['Leather', 14], []],
    
    ['kosciany helm', 0x1451, gump(64, 2), ['Leather', 4], ['Bone', 2]],
    ['kosciane rekawice', 0x1450, gump(64, 9), ['Leather', 6], ['Bone', 2]],
    ['kosciane naramienniki', 0x144E, gump(64, 16), ['Leather', 8], ['Bone', 4]],
    ['kosciane nakolanniki', 0x1452, gump(64, 23), ['Leather', 10], ['Bone', 6]],
    ['kosciana tunika', 0x144F, gump(64, 30), ['Leather', 12], ['Bone', 10]],
]

blacksmithInternalBase = [
#   [Name, TypeId, [GumpGroup, GumpItem], [Rersource1Name, Resource1Amount], [Rersource2Name, Resource2Amount] ]
    #['nnnazwa',    0xffff, [99, 9999], ['Cloth', 33], []],
    
    #['sierp',   XXXXX, gump(36, 2), ['Iron', 999], []],
    ['palasz',   0x0F5E, gump(36, 9), ['Iron', 10], []],
    #['polokragle ostrza',   XXXXX, gump(36, 16), ['Iron', 999], []],
    ['kordelas',   0x1441, gump(36, 23), ['Iron', 8], []],
    ['sztylet',   0x0F52, gump(36, 30), ['Iron', 3], []],
    ['krotki miecz',   0x13FF, gump(36, 37), ['Iron', 8], []],
    ['krys',   0x1401, gump(36, 44), ['Iron', 8], []],
    ['dlugi miecz',   0x0F61, gump(36, 51), ['Iron', 12], []],
    ['sejmitar',   0x13B6, gump(36, 58), ['Iron', 10], []],
    ['miecz poltorareczny',   0x13B9, gump(36, 65), ['Iron', 14], []],
    
    ['topor',   0x0F49, gump(43, 2), ['Iron', 14], []],
    ['topor bitewny',   0x0F47, gump(43, 9), ['Iron', 14], []],
    ['podwojny topor',   0x0F4B, gump(43, 16), ['Iron', 12], []],
    ['katowski topor',   0x0F45, gump(43, 23), ['Iron', 14], []],
    ['duzy bojowy topor',   0x13FB, gump(43, 30), ['Iron', 12], []],
    ['dwureczny topor',   0x1443, gump(43, 37), ['Iron', 16], []],
    ['topor bojowy',   0x13B0, gump(43, 44), ['Iron', 16], []],
    #['zdobiony topor',   0xffff, gump(43, 51), ['Iron', 18], []],
    
    ['basinet',        0x140C, gump(22, 2), ['Iron', 15], []],
    ['zamkniety helm', 0x1408, gump(22, 9), ['Iron', 15], []],
    ['helm',           0x140A, gump(22, 16), ['Iron', 15], []],
    ['helm nosowy',    0x140E, gump(22, 23), ['Iron', 15], []],
    ['plytowy helm',   0x1412, gump(22, 30), ['Iron', 15], []],
    
    #['bron drzewcowa',   0xfff, gump(50, 9999999999), ['Iron', 8], []],
    
    ['nadziak',   0x143D, gump(57, 2), ['Iron', 16], []],
    ['bulawa',   0x0F5C, gump(57, 9), ['Iron', 6], []],
    ['mlot bojowy',   0x143B, gump(57, 16), ['Iron', 10], []],
    ['berlo',   0x26BC, gump(57, 23), ['Iron',10], []],
    ['maczuga bojowa',   0x1407, gump(57, 30), ['Iron', 14], []],
    ['kafar',   0x1439, gump(57, 37), ['Iron', 16], []],
    
    ['kolczy czepiec',   0x13BB, gump(8, 2), ['Iron', 10], []],
    ['kolcze nogawice',   0x13BE, gump(8, 9), ['Iron', 18], []],
    ['kolczuga',   0x13BF, gump(8, 16), ['Iron', 20], []],
    
    ['pierscieniowe rekawice',   0x13EB, gump(1, 2), ['Iron', 10], []],
    ['pierscieniowe nogawice',   0x13F0, gump(1, 9), ['Iron', 16], []],
    ['pierscieniowe naramienniki',   0x13EE, gump(1, 16), ['Iron', 14], []],
    ['pierscieniowa tunika',   0x13EC, gump(1, 23), ['Iron', 18], []],
    
    ['kobieca zbroja plytowa',   0x1C04, gump(15, 37), ['Iron', 20], []],
    ['plytowe naramienniki', 0x1410, gump(15, 2), ['Iron', 18], []],
    ['plytowe rekawice', 0x1414, gump(15, 9), ['Iron', 12], []],
    ['plytowy karczek', 0x1413, gump(15, 16), ['Iron', 10], []],
    ['plytowe nogawice', 0x1411, gump(15, 23), ['Iron', 20], []],
    ['plytowy napiersnik', 0x1415, gump(15, 30), ['Iron', 25], []],
    
    ['puklerz', 0x1B73, gump(29, 2), ['Iron', 10], []],
    ['okragla tarcza', 0x1B72, gump(29, 9), ['Iron', 12], []],
    ['pawez', 0x1B76, gump(29, 16), ['Iron', 18], []],
    ['tarcza', 0x1B7B, gump(29, 23), ['Iron', 14], []],
    ['trojkatna tarcza', 0x1B74, gump(29, 30), ['Iron', 16], []],
    ['drewniana trojkatna tarcza', 0x1B79, gump(29, 37), ['Iron', 8], []],
    ['tarcza chaosu', 0x1BC3, gump(29, 44), ['Iron', 25], []],
    ['tarcza ladu', 0x1BC4, gump(29, 51), ['Iron', 25], []],
    
    ['berdysz', 0x0F4D, gump(50, 2), ['Iron', 18], []],
    #['glewia', 0xfff, gump(50, 9), ['Iron', 9999], []],
    #['ostrzana laska', 0xfff, gump(50, 16), ['Iron', 9999], []],
    ['halabarda', 0x143E, gump(50, 23), ['Iron', 20], []],
    #['lanca', 0xfff, gump(50, 30), ['Iron', 9999], []],
    #['pika', 0xfff, gump(50, 37), ['Iron', 9999], []],
    ['krotka wlocznia', 0x1403, gump(50, 44), ['Iron', 6], []],
    #['kosa', 0xfff, gump(50, 51), ['Iron', 9999], []],
    ['wlocznia', 0x0F62, gump(50, 58), ['Iron', 12], []],
    ['widly bojowe', 0x1405, gump(50, 65), ['Iron', 12], []],
    
    
]

fletcherInternalBase = [
    ['luk',                     0x13B2, gump(22,  2), ['RegularWood', 8], ['BowstringLeather', 1]],
    ['luk kompozytowy',         0x26C2, gump(22,  9), ['RegularWood', 9], ['BowstringLeather', 1]],
    ['starozytny luk',          0x27A5, gump(22, 16), ['RegularWood', 10], ['BowstringLeather', 1]],
    ['kusza',                   0x0F50, gump(22, 23), ['RegularWood', 8], ['BowstringLeather', 1]],
    ['ciezka kusza',            0x13FD, gump(22, 30), ['RegularWood', 9], ['BowstringLeather', 1]],
    ['powtarzalna kusza',       0x26C3, gump(22, 37), ['RegularWood', 10], ['BowstringLeather', 1]],
    ['magical shortbow',        0x2D2B, gump(22, 44), ['RegularWood', 15], ['BowstringLeather', 1]],
    ['elven composite longbow', 0x2D1E, gump(22, 51), ['RegularWood', 20], ['BowstringLeather', 1]],
]

#----------------------------------

blacksmithRewardsSmall = {}
blacksmithRewardsBig = {
    'ringmail': { # pierscieniowe
        'norm': {
            'Iron': {
                10: '-',
                15: '-',
                20: '-'
            },
            'Dull Copper': {
                10: '-',
                15: '-',
                20: 'powder'
            },
            'Shadow': {
                10: 'powder',
                15: 'powder',
                20: 'runic dull'
            },
            'Copper': {
                10: 'runic dull',
                15: 'runic dull',
                20: 'runic shadow'
            },
            'Bronze': {
                10: 'runic shadow',
                15: 'runic shadow',
                20: 'runic copper'
            },
            'Gold': {
                10: 'runic copper',
                15: 'runic copper',
                20: 'runic bronze'
            },
            'Agapite': {
                10: 'runic bronze',
                15: 'runic bronze',
                20: 'runic gold'
            },
            'Verite': {
                10: 'runic gold',
                15: 'runic gold',
                20: 'ancient 10'
            },
            'Valorite': {
                10: 'ancient 10',
                15: 'ancient 10',
                20: 'PS 15'
            },
        },
        'exp': {
            'Iron': {
                10: '-',
                15: '-',
                20: 'powder'
            },
            'Dull Copper': {
                10: 'runic copper',
                15: 'runic copper',
                20: 'runic bronze'
            },
            'Shadow': {
                10: 'runic bronze',
                15: 'runic bronze',
                20: 'runic gold'
            },
            'Copper': {
                10: 'runic gold',
                15: 'runic gold',
                20: 'ancient 10'
            },
            'Bronze': {
                10: 'ancient 10',
                15: 'ancient 10',
                20: 'PS 15'
            },
            'Gold': {
                10: 'PS 15',
                15: 'PS 15',
                20: 'ancient 15'
            },
            'Agapite': {
                10: 'ancient 15',
                15: 'ancient 15',
                20: 'PS 20'
            },
            'Verite': {
                10: 'PS 20',
                15: 'PS 20',
                20: 'runic agapite'
            },
            'Valorite': {
                10: 'runic agapite',
                15: 'runic agapite',
                20: 'ancient 30'
            },
        }
    },
    'chainmail': {  # kolcze
        'norm': {
            'Iron': {
                10: '-',
                15: '-',
                20: '-'
            },
            'Dull Copper': {
                10: 'runic dull',
                15: 'runic dull',
                20: 'runic shadow'
            },
            'Shadow': {
                10: 'runic shadow',
                15: 'runic shadow',
                20: 'runic copper'
            },
            'Copper': {
                10: 'runic copper',
                15: { 60: 'PS 5', 30: 'runic shadow' },
                20: 'runic bronze'
            },
            'Bronze': {
                10: 'runic bronze',
                15: 'runic bronze',
                20: { 60: 'PS 10', 30: 'runic gold' }
            },
            'Gold': {
                10: 'runic gold',
                15: 'runic gold',
                20: 'ancient 10'
            },
            'Agapite': {
                10: 'ancient 10',
                15: 'ancient 10',
                20: 'PS 15'
            },
            'Verite': {
                10: 'PS 15',
                15: 'PS 15',
                20: 'ancient 15'
            },
            'Valorite': {
                10: 'ancient 15',
                15: 'ancient 15',
                20: 'PS 20'
            },
        },
        'exp': {
            'Iron': {
                10: 'runic dull',
                15: 'runic dull',
                20: 'runic shadow'
            },
            'Dull Copper': {
                10: 'runic gold',
                15: 'runic gold',
                20: 'ancient 10'
            },
            'Shadow': {
                10: 'ancient 10',
                15: 'ancient 10',
                20: 'PS 15'
            },
            'Copper': {
                10: 'PS 15',
                15: 'PS 15',
                20: 'ancient 15'
            },
            'Bronze': {
                10: 'ancient 15',
                15: 'ancient 15',
                20: 'PS 20'
            },
            'Gold': {
                10: 'PS 20',
                15: 'PS 20',
                20: 'runic agapite'
            },
            'Agapite': {
                10: 'runic agapite',
                15: 'runic agapite',
                20: 'ancient 30'
            },
            'Verite': {
                10: 'ancient 30',
                15: 'ancient 30',
                20: 'runic verite'
            },
            'Valorite': {
                10: 'runic verite',
                15: 'runic verite',
                20: 'ancient 60'
            },
        }
    },
    'platemail': {
        'norm': {
            'Iron': {
                10: '-',
                15: '-',
                20: 'powder'
            },
            'Dull Copper': {
                10: 'runic copper',
                15: {60: 'PS 5', 30: 'runic shadow'},
                20: 'runic bronze'
            },
            'Shadow': {
                10: 'runic bronze',
                15: {60: 'PS 10', 30: 'runic copper'},
                20: 'runic gold'
            },
            'Copper': {
                10: 'runic gold',
                15: 'runic gold',
                20: 'ancient 10'
            },
            'Bronze': {
                10: 'ancient 10',
                15: 'ancient 10',
                20: 'PS 15'
            },
            'Gold': {
                10: 'PS 15',
                15: 'PS 15',
                20: 'ancient 15'
            },
            'Agapite': {
                10: 'ancient 15',
                15: 'ancient 15',
                20: 'PS 20'
            },
            'Verite': {
                10: 'PS 20',
                15: 'PS 20',
                20: 'runic agapite'
            },
            'Valorite': {
                10: 'runic agapite',
                15: 'runic agapite',
                20: 'ancient 30'
            },
        },
        'exp': {
            'Iron': {
                10: 'runic copper',
                15: {60: 'PS 5', 30: 'runic shadow'},
                20: 'runic bronze'
            },
            'Dull Copper': {
                10: 'PS 15',
                15: 'PS 15',
                20: 'ancient 15'
            },
            'Shadow': {
                10: 'ancient 15',
                15: 'ancient 15',
                20: 'PS 20'
            },
            'Copper': {
                10: 'PS 20',
                15: 'PS 20',
                20: 'runic agapite'
            },
            'Bronze': {
                10: 'runic agapite',
                15: 'runic agapite',
                20: 'ancient 30'
            },
            'Gold': {
                10: 'ancient 30',
                15: 'ancient 30',
                20: 'runic verite'
            },
            'Agapite': {
                10: 'runic verite',
                15: 'runic verite',
                20: 'ancient 60'
            },
            'Verite': {
                10: 'ancient 60',
                15: 'ancient 60',
                20: 'runic valorite'
            },
            'Valorite': {
                10: 'runic valorite',
                15: 'runic valorite',
                20: 'runic valorite'
            },
        }
    }
}

#----------------------------------

resource1IdByProductId = {}
resource2IdByProductId = {}
resource1HueByProductId = {}
resource2HueByProductId = {}

def fillResourceDataForEntry(entry):
    productId = entry[1]
    resType = entry[3][0]
    if resType in resourcesId.keys():
        resource1IdByProductId[productId] = resourcesId[resType]
    if resType in resourcesHue.keys():
        resource1HueByProductId[productId] = resourcesHue[resType]
    if len(entry[4]) > 0:
        resType = entry[4][0]
        if resType in resourcesId.keys():
            resource2IdByProductId[productId] = resourcesId[resType]
        if resType in resourcesHue.keys():
            resource2HueByProductId[productId] = resourcesHue[resType]

tailorGumpByProductId = {}
tailorProductIdByName = {}
tailorResource1AmountByProductId = {}
tailorResource2AmountByProductId = {}

for entry in tailorInternalBase:
    tailorGumpByProductId[entry[1]] = entry[2]
    tailorProductIdByName[entry[0]] = entry[1]
    tailorResource1AmountByProductId[entry[1]] = entry[3][1]
    if len(entry[4]) > 0:
        tailorResource2AmountByProductId[entry[1]] = entry[4][1]
    else:
        tailorResource2AmountByProductId[entry[1]] = 0
    
    fillResourceDataForEntry(entry)

blacksmithGumpByProductId = {}
blacksmithProductIdByName = {}
blacksmithResource1AmountByProductId = {}
blacksmithResource2AmountByProductId = {}

for entry in blacksmithInternalBase:
    blacksmithGumpByProductId[entry[1]] = entry[2]
    blacksmithProductIdByName[entry[0]] = entry[1]
    blacksmithResource1AmountByProductId[entry[1]] = entry[3][1]
    if len(entry[4]) > 0:
        blacksmithResource2AmountByProductId[entry[1]] = entry[4][1]
    else:
        blacksmithResource2AmountByProductId[entry[1]] = 0
    
    fillResourceDataForEntry(entry)

fletcherGumpByProductId = {}
fletcherProductIdByName = {}
fletcherResource1AmountByProductId = {}
fletcherResource2AmountByProductId = {}

for entry in fletcherInternalBase:
    fletcherGumpByProductId[entry[1]] = entry[2]
    fletcherProductIdByName[entry[0]] = entry[1]
    fletcherResource1AmountByProductId[entry[1]] = entry[3][1]
    if len(entry[4]) > 0:
        fletcherResource2AmountByProductId[entry[1]] = entry[4][1]
    else:
        fletcherResource2AmountByProductId[entry[1]] = 0
    
    fillResourceDataForEntry(entry)