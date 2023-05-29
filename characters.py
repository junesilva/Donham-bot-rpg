races_dict = {
    'Humano': {
        'nome': 'Humano',
        'description': 'Os humanos são uma raça versátil e adaptável, conhecida por sua diversidade e capacidade de se destacar em várias áreas.',
        'habilidades_primarias': 'Escolha duas habilidades primárias',
        'bonus_habilidades': '',
        'bonus_caracteristicas': ''
    },
    'Elfo': {
        'nome': 'Elfo',
        'description': 'Os elfos são uma raça graciosa e longeva, conhecida por sua agilidade e afinidade com a magia e a natureza.',
        'habilidades_primarias': 'Destreza, Sabedoria',
        'bonus_habilidades': 'Visão no Escuro, Resistência a encantamentos mágicos',
        'bonus_caracteristicas': ''
    },
    'Anão': {
        'nome': 'Anão',
        'description': 'Os anões são uma raça robusta e resistente, conhecida por sua força e habilidade na construção e no combate.',
        'habilidades_primarias': 'Constituição, Sabedoria',
        'bonus_habilidades': 'Visão no Escuro, Resistência a veneno',
        'bonus_caracteristicas': ''
    },
    'Halfling': {
        'nome': 'Halfling',
        'description': 'Os halflings são uma raça pequena e ágil, conhecida por sua sorte e habilidade em evitar perigos.',
        'habilidades_primarias': 'Destreza, Carisma',
        'bonus_habilidades': 'Sorte, Agilidade Halfling',
        'bonus_caracteristicas': ''
    },
    'Draconato': {
        'nome': 'Draconato',
        'description': 'Os draconatos são uma raça com sangue de dragão, conhecida por sua presença majestosa e habilidades draconicas.',
        'habilidades_primarias': 'Força, Carisma',
        'bonus_habilidades': 'Sopro de Dragão, Resistência a dano',
        'bonus_caracteristicas': ''
    },
    'Gnomo': {
        'nome': 'Gnomo',
        'description': 'Os gnomos são uma raça curiosa e engenhosa, conhecida por sua inteligência e habilidade com magia e tecnologia.',
        'habilidades_primarias': 'Inteligência, Destreza',
        'bonus_habilidades': 'Visão no Escuro, Esperteza Gnômica',
        'bonus_caracteristicas': ''
    },
    'Meio-Elfo': {
        'nome': 'Meio-Elfo',
        'description': 'Os meio-elfos são uma mistura de humanos e elfos, conhecidos por sua versatilidade e habilidades sociais.',
        'habilidades_primarias': 'Carisma, Duas habilidades primárias à escolha',
        'bonus_habilidades': 'Visão no Escuro, Imunidade a encantamentos do sono',
        'bonus_caracteristicas': ''
    },
    'Meio-Orc': {
        'nome': 'Meio-Orc',
        'description': 'Os meio-orcs são uma mistura de humanos e orcs, conhecidos por sua força bruta e resistência.',
        'habilidades_primarias': 'Força, Constituição',
        'bonus_habilidades': 'Visão no Escuro, Ferocidade Relentless',
        'bonus_caracteristicas': ''
    },
    'Tiefling': {
        'nome': 'Tiefling',
        'description': 'Os tieflings são uma raça com sangue demoníaco, conhecidos por sua aparência marcante e habilidades infernais.',
        'habilidades_primarias': 'Carisma, Inteligência',
        'bonus_habilidades': 'Visão no Escuro, Resistência a fogo',
        'bonus_caracteristicas': ''
    }
}

classes_dict = {
        'Guerreiro': {
            'nome': 'Guerreiro',
            'description': 'O Guerreiro é um combatente corpo a corpo especializado em lidar dano físico. Possui habilidades que o tornam resistente e eficiente em combate.',
            'vida': 'd10',
        },
        'Mago': {
            'nome': 'Mago',
            'description': 'O Mago é um manipulador de magia com um vasto conhecimento dos segredos arcanos. Possui habilidades mágicas poderosas e versáteis.',
            'vida': 'd6',
        },
        'Ladino': {
            'nome': 'Ladino',
            'description': 'O Ladino é especialista em furtividade, agilidade e enganação. Possui habilidades que o tornam hábil em ataques furtivos e em desarmar armadilhas.',
            'vida': 'd8',
        },
        'Clérigo': {
            'nome': 'Clérigo',
            'description': 'O Clérigo é um seguidor devoto de uma divindade, capaz de invocar poderes divinos para curar ferimentos e banir criaturas malignas. Possui habilidades de suporte e cura.',
            'vida': 'd8',
        },
        'Bárbaro': {
            'nome': 'Bárbaro',
            'description': 'O Bárbaro é um lutador feroz e indomável. Possui habilidades que o tornam mais resistente e mais poderoso quando enfurecido. É especializado em combate corpo a corpo.',
            'vida': 'd12',
        },
        'Bardo': {
            'nome': 'Bardo',
            'description': 'O Bardo é um artista versátil e um contador de histórias habilidoso. Possui habilidades mágicas e inspiradoras que podem influenciar seus aliados e manipular as emoções dos outros.',
            'vida': 'd8',
        },
        'Druida': {
            'nome': 'Druida',
            'description': 'O Druida é um guardião da natureza e um manipulador dos elementos. Possui habilidades mágicas relacionadas à natureza, podendo se transformar em animais e invocar a força da terra.',
            'vida': 'd8',
        },
        'Feiticeiro': {
            'nome': 'Feiticeiro',
            'description': 'O Feiticeiro é um usuário nato de magia, cujos poderes são inatos e não derivados de estudos. Possui habilidades mágicas poderosas e espontâneas.',
            'vida': 'd6',
        },
        'Monge': {
            'nome': 'Monge',
            'description': 'O Monge é um mestre das artes marciais e disciplinado em sua mente e corpo. Possui habilidades que o permitem desferir golpes rápidos e precisos.',
            'vida': 'd8',
        },
        'Paladino': {
            'nome': 'Paladino',
            'description': 'O Paladino é um guerreiro sagrado dedicado a um código de honra e justiça. Possui habilidades mágicas divinas e pode curar ferimentos além de combater o mal.',
            'vida': 'd10',
        },
        'Patrulheiro': {
            'nome': 'Patrulheiro',
            'description': 'O Patrulheiro é um explorador habilidoso e um mestre das terras selvagens. Possui habilidades de rastreamento, sobrevivência e combate à distância.',
            'vida': 'd10',
        },
    }